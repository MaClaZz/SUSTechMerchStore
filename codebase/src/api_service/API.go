// DEPENDENCIES-----
import (
    "context"
    "log"
    "net/http"
    "time"
    "encoding/json"
    "github.com/gorilla/mux"
    "github.com/dgrijalva/jwt-go"
    "google.golang.org/grpc"
    pb "path/to/generated/protos" // Update this to your proto location
)

// JWT SETUP-----
var jwtKey = []byte("your_jwt_secret_key") // Use a strong key
type Claims struct {
    Username string `json:"username"`
    jwt.StandardClaims
}

// Middleware to authenticate JWT tokens
func authenticate(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        tokenStr := r.Header.Get("Authorization")[7:] // Strip "Bearer "
        claims := &Claims{}

        token, err := jwt.ParseWithClaims(tokenStr, claims, func(token *jwt.Token) (interface{}, error) {
            return jwtKey, nil
        })

        if err != nil || !token.Valid {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        next.ServeHTTP(w, r)
    })
}

//gRPC Client Setup-----
var grpcClient pb.DBServiceClient
func init() {
    conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
    if err != nil {
        log.Fatalf("Failed to connect: %v", err)
    }
    grpcClient = pb.NewDBServiceClient(conn)
}
//Routes and Handlers-----
func main() {
    r := mux.NewRouter()

    r.HandleFunc("/", greet).Methods("GET")
    r.Handle("/products", authenticate(http.HandlerFunc(listProducts))).Methods("GET")
    r.HandleFunc("/register", register).Methods("POST")
    r.HandleFunc("/login", login).Methods("POST")

    log.Println("Server started on :8080")
    http.ListenAndServe(":8080", r)
}

// Greeting handler
func greet(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(context.Background(), time.Second)
    defer cancel()

    resp, err := grpcClient.Greet(ctx, &pb.Empty{})
    if err != nil {
        http.Error(w, "Error in greeting", http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(map[string]string{"message": resp.Message})
}

//Product List Example------
func listProducts(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(context.Background(), time.Second)
    defer cancel()

    resp, err := grpcClient.ListProducts(ctx, &pb.Empty{})
    if err != nil {
        http.Error(w, "Failed to fetch products", http.StatusInternalServerError)
        return
    }

    json.NewEncoder(w).Encode(resp.Products) // Adjust this based on your proto definition
}

// User Registration Example-----
func register(w http.ResponseWriter, r *http.Request) {
    var user pb.RegisterRequest
    err := json.NewDecoder(r.Body).Decode(&user)
    if err != nil {
        http.Error(w, "Invalid input", http.StatusBadRequest)
        return
    }

    ctx, cancel := context.WithTimeout(context.Background(), time.Second)
    defer cancel()

    // Hash password (add bcrypt logic here)
    resp, err := grpcClient.Register(ctx, &user)
    if err != nil {
        http.Error(w, "Failed to register", http.StatusInternalServerError)
        return
    }

    json.NewEncoder(w).Encode(resp)
}

/*Additional Notes:
gRPC Protobuf Generation: Use protoc to generate Go code from .proto files.
Logging: Replace the log_queue with a Go channel and run log handling as a goroutine.
Error Handling: Implement more robust error handling and validation.
Concurrency: Use goroutines for parallel tasks (similar to Python's threading).
This structure ensures your Go server communicates with gRPC, handles authentication, and serves endpoints as your Python code does. Adjust paths, imports, and specific logic based on your setup!*/