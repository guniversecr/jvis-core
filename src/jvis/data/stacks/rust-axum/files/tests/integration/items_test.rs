//! Integration tests for Item CRUD endpoints.

#[cfg(test)]
mod tests {
    use axum::http::StatusCode;
    use serde_json::json;

    // These tests require a running database.
    // Run with: cargo test -- --ignored

    #[tokio::test]
    #[ignore]
    async fn test_create_item() {
        let client = reqwest::Client::new();
        let res = client
            .post("http://localhost:8000/api/items")
            .json(&json!({"name": "Test Item", "description": "A test"}))
            .send()
            .await
            .unwrap();

        assert_eq!(res.status(), StatusCode::CREATED);
        let body: serde_json::Value = res.json().await.unwrap();
        assert_eq!(body["name"], "Test Item");
        assert!(body["id"].is_string());
    }

    #[tokio::test]
    #[ignore]
    async fn test_list_items() {
        let client = reqwest::Client::new();
        let res = client
            .get("http://localhost:8000/api/items")
            .send()
            .await
            .unwrap();

        assert_eq!(res.status(), StatusCode::OK);
        let body: serde_json::Value = res.json().await.unwrap();
        assert!(body.is_array());
    }

    #[tokio::test]
    #[ignore]
    async fn test_get_nonexistent_returns_404() {
        let client = reqwest::Client::new();
        let res = client
            .get("http://localhost:8000/api/items/00000000-0000-0000-0000-000000000000")
            .send()
            .await
            .unwrap();

        assert_eq!(res.status(), StatusCode::NOT_FOUND);
    }
}
