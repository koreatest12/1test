import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class MassiveClaudeAgent {

    private static final String CLAUDE_API_URL = "https://api.anthropic.com/v1/messages";
    private static final String ANTHROPIC_VERSION = "2023-06-01";
    private final String apiKey;
    private final HttpClient httpClient;
    
    // [동시성 제어] 최대 50개의 스레드를 재사용하여 중복 및 동시 수행
    private final ExecutorService executor = Executors.newFixedThreadPool(50);
    
    // [Rate Limit 방어] 초당 API 요청 수를 제한하기 위한 세마포어 (예: 동시 5개까지만 통신 허용)
    private final Semaphore rateLimiter = new Semaphore(5); 

    public MassiveClaudeAgent() {
        this.apiKey = System.getenv("ANTHROPIC_API_KEY");
        // 파이프라인(CI/CD) 환경에서는 키가 없어도 빌드가 터지지 않도록 Mock 모드 지원
        if (this.apiKey == null || this.apiKey.isBlank()) {
            System.err.println("[WARN] ANTHROPIC_API_KEY가 없습니다. Mock(가짜) 데이터 생성 모드로 동작합니다.");
        }

        this.httpClient = HttpClient.newBuilder()
                .executor(executor) // 커스텀 스레드 풀 주입
                .connectTimeout(Duration.ofSeconds(15))
                .build();
    }

    public CompletableFuture<String> callClaudeApi(String prompt) {
        if (this.apiKey == null || this.apiKey.isBlank()) {
            // Mock 데이터 생성 (API 키 누락 시 GitHub Actions 실패 방지)
            return CompletableFuture.completedFuture(
                "{\"status\":\"mock\", \"data\":\"" + prompt.hashCode() + "\"}"
            );
        }

        String jsonPayload = String.format(
            "{\"model\": \"claude-3-haiku-20240307\", \"max_tokens\": 150, \"messages\": [{\"role\": \"user\", \"content\": \"%s\"}]}", 
            prompt.replace("\"", "\\\"")
        );

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(CLAUDE_API_URL))
                .header("Content-Type", "application/json")
                .header("x-api-key", this.apiKey)
                .header("anthropic-version", ANTHROPIC_VERSION)
                .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                .build();

        return CompletableFuture.supplyAsync(() -> {
            try {
                rateLimiter.acquire(); // 동시 요청 수 제한 획득
                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 429) {
                    System.err.println("[WARN] Rate Limit 초과 (429). 5초 대기 후 재시도 필요.");
                    Thread.sleep(5000); // 429 에러 시 백오프 대기
                } else if (response.statusCode() != 200) {
                    throw new RuntimeException("HTTP " + response.statusCode() + ": " + response.body());
                }
                return response.body();
            } catch (Exception e) {
                throw new CompletionException(e);
            } finally {
                rateLimiter.release(); // 요청 완료 후 제한 해제
            }
        }, executor);
    }

    public void generateMassResources(int totalCount, int batchSize) {
        System.out.println("[Mass Generator] 총 " + totalCount + "건의 AI 리소스를 배치 사이즈 " + batchSize + " 단위로 동시/중복 생성합니다...");
        
        Path outputDir = Paths.get("generated/data/ai_seed");
        try {
            Files.createDirectories(outputDir);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        // Batch 단위로 분할하여 중복 수행 및 메모리 오버플로우 방지
        for (int batch = 0; batch < totalCount; batch += batchSize) {
            int currentBatchEnd = Math.min(batch + batchSize, totalCount);
            System.out.println(" -> Processing Batch [" + batch + " ~ " + (currentBatchEnd - 1) + "]");

            List<CompletableFuture<Void>> futures = IntStream.range(batch, currentBatchEnd)
                    .mapToObj(i -> {
                        String prompt = "마이크로서비스 Fencing 노드 데이터 생성을 위한 무작위 방화벽 룰 1개를 JSON 형식으로만 응답해줘. (ID: RULE-" + i + ")";
                        
                        return callClaudeApi(prompt).thenAccept(result -> {
                            saveToFile(outputDir, "rule_" + i + ".json", result);
                        }).exceptionally(ex -> {
                            System.err.println("[FAILED] ID: " + i + " - " + ex.getMessage());
                            return null;
                        });
                    })
                    .collect(Collectors.toList());

            // 현재 배치의 모든 동시 작업이 끝날 때까지 대기
            CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
        }

        executor.shutdown();
        System.out.println("[Mass Generator] 대량 리소스 생성이 완벽히 종료되었습니다.");
    }

    private void saveToFile(Path dir, String fileName, String content) {
        try {
            Files.writeString(dir.resolve(fileName), content + "\n", 
                StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
        } catch (IOException e) {
            System.err.println("파일 쓰기 실패: " + fileName);
        }
    }

    public static void main(String[] args) {
        MassiveClaudeAgent agent = new MassiveClaudeAgent();
        // 500건의 데이터를 100건 단위 묶음(Batch)으로 중복/동시 실행 수행
        // (실제 GitHub Actions에서 수만 건을 API로 쏘면 과금이 폭탄이 될 수 있으므로, 테스트용 500건 설정)
        agent.generateMassResources(500, 100); 
    }
}
