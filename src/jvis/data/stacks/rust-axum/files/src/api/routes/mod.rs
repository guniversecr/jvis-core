pub mod health;
pub mod items;

use axum::Router;

use crate::infrastructure::database::DbPool;

pub fn create_router() -> Router<DbPool> {
    Router::new().merge(health::router()).merge(items::router())
}
