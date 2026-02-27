use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct CreateItemDto {
    pub name: String,
    pub description: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct UpdateItemDto {
    pub name: Option<String>,
    pub description: Option<String>,
}
