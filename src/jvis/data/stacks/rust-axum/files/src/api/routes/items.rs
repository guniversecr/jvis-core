use axum::extract::{Path, State};
use axum::http::StatusCode;
use axum::routing::{get, post};
use axum::{Json, Router};
use uuid::Uuid;

use crate::application::dto::{CreateItemDto, UpdateItemDto};
use crate::application::services::ItemService;
use crate::domain::entities::Item;
use crate::domain::errors::AppError;
use crate::infrastructure::database::DbPool;

pub fn router() -> Router<DbPool> {
    Router::new()
        .route("/api/items", get(list_items).post(create_item))
        .route(
            "/api/items/:id",
            get(get_item).patch(update_item).delete(delete_item),
        )
}

async fn create_item(
    State(pool): State<DbPool>,
    Json(dto): Json<CreateItemDto>,
) -> Result<(StatusCode, Json<Item>), AppError> {
    if dto.name.is_empty() {
        return Err(AppError::Validation("name is required".to_string()));
    }
    let item = ItemService::create(&pool, dto).await?;
    Ok((StatusCode::CREATED, Json(item)))
}

async fn list_items(State(pool): State<DbPool>) -> Result<Json<Vec<Item>>, AppError> {
    let items = ItemService::list(&pool).await?;
    Ok(Json(items))
}

async fn get_item(
    State(pool): State<DbPool>,
    Path(id): Path<Uuid>,
) -> Result<Json<Item>, AppError> {
    let item = ItemService::get_by_id(&pool, id).await?;
    Ok(Json(item))
}

async fn update_item(
    State(pool): State<DbPool>,
    Path(id): Path<Uuid>,
    Json(dto): Json<UpdateItemDto>,
) -> Result<Json<Item>, AppError> {
    let item = ItemService::update(&pool, id, dto).await?;
    Ok(Json(item))
}

async fn delete_item(
    State(pool): State<DbPool>,
    Path(id): Path<Uuid>,
) -> Result<StatusCode, AppError> {
    ItemService::delete(&pool, id).await?;
    Ok(StatusCode::NO_CONTENT)
}
