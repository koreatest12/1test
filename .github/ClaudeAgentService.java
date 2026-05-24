import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class ClaudeAgentService {

    private static final String CLAUDE_API_URL = "https://api.anthropic.com/v1/messages";
    private static final String ANTHROPIC_VERSION = "2023-06-01"; // 필수 헤더
    private final String apiKey;
    private final HttpClient httpClient;

    public ClaudeAgentService() {
        // 보안을 위해 API 키는 환경변수에서 로드합니다.
        this.apiKey = System.getenv("ANTHROPIC_API_KEY");
        if (this.apiKey == null || this.apiKey.isBlank()) {
            throw new IllegalStateException("환경변수 'ANTHROPIC_API_KEY'가 설정되지 않았습니다.");
        }

        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();
    }

    /**
     * [에러 수정됨] Claude API 비동기 호출 메서드
     * x-api-key 와 anthropic-version 헤더가 정상적으로 주입됩니다.
     */
    public CompletableFuture<String> callClaudeApi(String prompt) {
        String jsonPayload = String.format(
            "{\"model\": \"claude-3-haiku-20240307\", \"max_tokens\": 1024, \"messages\": [{\"role\": \"user\", \"content\": \"%s\"}]}", 
            prompt.replace("\"", "\\\"") // JSON 이스케이프 처리
        );

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(CLAUDE_API_URL))
                .header("Content-Type", "application/json")
                .header("x-api-key", this.apiKey)              // 💡 401 에러 해결 핵심
                .header("anthropic-version", ANTHROPIC_VERSION) // 💡 401 에러 해결 핵심
                .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                .build();

        return httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(response -> {
                    if (response.statusCode() != 200) {
                        throw new RuntimeException("HTTP " + response.statusCode() + ": " + response.body());
                    }
                    return response.body();
                });
    }

    /**
     * [대량 생성 반영] 비동기 동시성(Concurrency)을 활용한 데이터 대량 생성
     * @param count 생성할 데이터 세트의 수
     */
    public void generateMassResources(int count) {
        System.out.println("[Mass Generation] " + count + "개의 AI 데이터 리소스 동시 생성을 시작합니다...");

        // CompletableFuture를 이용해 여러 API 요청을 비동기적으로 동시 실행
        List<CompletableFuture<Void>> futures = IntStream.range(0, count)
                .mapToObj(i -> {
                    String prompt = "보안 마이크로서비스 노드 NODE-" + String.format("%04d", i) + "에 대한 가상의 접근 로그를 JSON 형식으로 1줄만 생성해줘.";
                    
                    return callClaudeApi(prompt)
                            .thenAccept(result -> {
                                System.out.println("[SUCCESS] 생성 완료 (Node-" + i + ") -> " + result.substring(0, Math.min(50, result.length())) + "...");
                            })
                            .exceptionally(ex -> {
                                System.err.println("[FAILED] 에러 발생 (Node-" + i + "): " + ex.getMessage());
                                return null;
                            });
                })
                .collect(Collectors.toList());

        // 모든 비동기 작업이 끝날 때까지 대기
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
        System.out.println("[Mass Generation] 대량 리소스 생성이 완료되었습니다.");
    }

    public static void main(String[] args) {
        try {
            ClaudeAgentService agent = new ClaudeAgentService();
            // 주의: API Rate Limit을 고려하여 대량 생성 수를 조절하세요 (예: 5개씩 테스트)
            agent.generateMassResources(5); 
            
        } catch (Exception e) {
            System.err.println("애플리케이션 오류: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
