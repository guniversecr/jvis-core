use axum::{routing::get, Json, Router};
use serde_json::{json, Value};

pub fn router() -> Router {
    Router::new()
        .route("/api/health", get(health_check))
        .route("/", get(root))
}

async fn health_check() -> Json<Value> {
    Json(json!({"status": "healthy"}))
}

async fn root() -> Json<Value> {
    Json(json!({"service": env!("CARGO_PKG_NAME"), "status": "running"}))
}
