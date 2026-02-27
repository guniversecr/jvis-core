"""Cross-stack integration tests for functional scaffolds (ADR-003).

Verifies that all 17 functional stacks generate correct, complete, and
consistent output.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from jvis.scaffold.stack_runner import run_stack
from jvis.stacks.registry import get_stack

FUNCTIONAL_STACKS = [
    "python-fastapi",
    "nodejs-express",
    "react-vite",
    "python-django",
    "python-flask",
    "nextjs",
    "rust-axum",
    "nodejs-fastify",
    "nodejs-nestjs",
    "php-laravel",
    "php-symfony",
    "nuxt",
    "angular",
    "vue-vite",
    "svelte-kit",
    "astro",
    "custom",
]


class TestFunctionalScaffoldGeneration:
    """Parameterized tests across all functional stacks."""

    @pytest.mark.parametrize("stack_id", FUNCTIONAL_STACKS)
    def test_stack_generates_without_errors(self, tmp_path: Path, stack_id: str) -> None:
        """All functional stacks should generate without exceptions."""
        stack = get_stack(stack_id)
        assert stack is not None, f"Stack '{stack_id}' not found in registry"

        db = "postgresql" if stack.requires_database else ""
        run_stack(stack, tmp_path, "test-project", "Test Project", db)

        # Verify key directories were created
        if stack_id == "python-django":
            assert (tmp_path / "core").is_dir(), f"{stack_id}: core/ directory missing"
        elif stack_id == "php-laravel":
            assert (tmp_path / "app").is_dir(), f"{stack_id}: app/ directory missing"
        elif stack_id == "nuxt":
            assert (tmp_path / "server").is_dir(), f"{stack_id}: server/ directory missing"
        else:
            assert (tmp_path / "src").is_dir(), f"{stack_id}: src/ directory missing"

    @pytest.mark.parametrize("stack_id", FUNCTIONAL_STACKS)
    def test_no_jinja2_artifacts(self, tmp_path: Path, stack_id: str) -> None:
        """No generated file should contain raw Jinja2 syntax."""
        stack = get_stack(stack_id)
        assert stack is not None

        db = "postgresql" if stack.requires_database else ""
        run_stack(stack, tmp_path, "test-project", "Test Project", db)

        text_extensions = {
            ".ts",
            ".tsx",
            ".js",
            ".jsx",
            ".py",
            ".json",
            ".yaml",
            ".yml",
            ".toml",
            ".cfg",
            ".ini",
            ".css",
            ".html",
            ".prisma",
            ".md",
            ".rs",
            ".sql",
            ".vue",
            ".svelte",
            ".astro",
            ".php",
        }

        for file_path in tmp_path.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix not in text_extensions:
                continue

            relative = file_path.relative_to(tmp_path)

            # Angular component templates use {{ expr }} for data binding (not Jinja2)
            if stack_id == "angular" and file_path.suffix == ".html" and "app" in relative.parts:
                continue

            # Vue SFC files use {{ expr }} for template interpolation (not Jinja2)
            if stack_id == "vue-vite" and file_path.suffix == ".vue":
                continue

            # Nuxt .vue files also use {{ expr }} for Vue template interpolation
            if stack_id == "nuxt" and file_path.suffix == ".vue":
                continue

            content = file_path.read_text(encoding="utf-8", errors="ignore")

            # Check for Jinja2 expression markers
            assert "{{" not in content, f"{stack_id}: Jinja2 expression '{{{{' found in {relative}"
            assert "{%" not in content, f"{stack_id}: Jinja2 statement '{{% ' found in {relative}"

    @pytest.mark.parametrize("stack_id", FUNCTIONAL_STACKS)
    def test_item_entity_consistency(self, tmp_path: Path, stack_id: str) -> None:
        """All stacks should have an Item entity with name and description fields."""
        stack = get_stack(stack_id)
        assert stack is not None

        db = "postgresql" if stack.requires_database else ""
        run_stack(stack, tmp_path, "test-project", "Test Project", db)

        # Find the Item entity/type/interface file
        item_paths = {
            "python-fastapi": tmp_path / "src" / "domain" / "entities" / "item.py",
            "nodejs-express": tmp_path / "src" / "domain" / "entities" / "item.ts",
            "react-vite": tmp_path / "src" / "types" / "item.ts",
            "python-django": tmp_path / "core" / "models.py",
            "python-flask": tmp_path / "src" / "models.py",
            "nextjs": tmp_path / "src" / "types" / "item.ts",
            "rust-axum": tmp_path / "src" / "domain" / "entities" / "item.rs",
            "nodejs-fastify": tmp_path / "src" / "domain" / "entities" / "item.ts",
            "nodejs-nestjs": tmp_path / "src" / "items" / "entities" / "item.entity.ts",
            "php-laravel": tmp_path / "app" / "Models" / "Item.php",
            "php-symfony": tmp_path / "src" / "Entity" / "Item.php",
            "nuxt": tmp_path / "types" / "item.ts",
            "angular": tmp_path / "src" / "app" / "models" / "item.model.ts",
            "vue-vite": tmp_path / "src" / "types" / "item.ts",
            "svelte-kit": tmp_path / "src" / "lib" / "types" / "item.ts",
            "astro": tmp_path / "src" / "types" / "item.ts",
            "custom": tmp_path / "src" / "models.py",
        }

        item_file = item_paths[stack_id]
        assert item_file.is_file(), f"{stack_id}: Item entity not found at {item_file}"

        content = item_file.read_text()
        assert "name" in content, f"{stack_id}: 'name' field missing from Item entity"
        assert "description" in content, f"{stack_id}: 'description' field missing from Item entity"


class TestDatabaseConditionals:
    """Tests for database-conditional template rendering."""

    @pytest.mark.parametrize("db_type", ["postgresql", "mysql", "sqlite"])
    def test_nodejs_express_prisma_provider(self, tmp_path: Path, db_type: str) -> None:
        """Prisma schema should use the correct provider for each database type."""
        stack = get_stack("nodejs-express")
        assert stack is not None

        run_stack(stack, tmp_path, "test-api", "Test API", db_type)

        schema = (tmp_path / "prisma" / "schema.prisma").read_text()

        if db_type == "sqlite":
            assert '"sqlite"' in schema
            assert "file:./dev.db" in schema
        else:
            assert f'"{db_type}"' in schema
            assert 'env("DATABASE_URL")' in schema

        # Item model should always be present regardless of DB type
        assert "model Item" in schema

    @pytest.mark.parametrize("db_type", ["postgresql", "mysql"])
    def test_python_fastapi_database_driver(self, tmp_path: Path, db_type: str) -> None:
        """Python FastAPI should use the correct async driver for each database."""
        stack = get_stack("python-fastapi")
        assert stack is not None

        run_stack(stack, tmp_path, "test-api", "Test API", db_type)

        # Check pyproject.toml for correct driver
        pyproject = (tmp_path / "pyproject.toml").read_text()

        if db_type == "postgresql":
            assert "asyncpg" in pyproject
        elif db_type == "mysql":
            assert "aiomysql" in pyproject

    @pytest.mark.parametrize("db_type", ["postgresql", "mysql", "sqlite"])
    def test_python_django_database_backend(self, tmp_path: Path, db_type: str) -> None:
        """Django should use the correct database backend for each type."""
        stack = get_stack("python-django")
        assert stack is not None

        run_stack(stack, tmp_path, "test-django", "Test Django", db_type)

        settings = (tmp_path / "config" / "settings.py").read_text()

        if db_type == "postgresql":
            assert "django.db.backends.postgresql" in settings
        elif db_type == "mysql":
            assert "django.db.backends.mysql" in settings
        else:
            assert "django.db.backends.sqlite3" in settings

    @pytest.mark.parametrize("db_type", ["postgresql", "mysql", "sqlite"])
    def test_python_flask_database_uri(self, tmp_path: Path, db_type: str) -> None:
        """Flask should use the correct SQLAlchemy URI for each database type."""
        stack = get_stack("python-flask")
        assert stack is not None

        run_stack(stack, tmp_path, "test-flask", "Test Flask", db_type)

        config = (tmp_path / "src" / "config.py").read_text()

        if db_type == "postgresql":
            assert "postgresql://" in config
        elif db_type == "mysql":
            assert "mysql+pymysql://" in config
        else:
            assert "sqlite:///" in config

    @pytest.mark.parametrize("db_type", ["postgresql", "mysql", "sqlite"])
    def test_nextjs_prisma_provider(self, tmp_path: Path, db_type: str) -> None:
        """Next.js Prisma schema should use the correct provider."""
        stack = get_stack("nextjs")
        assert stack is not None

        run_stack(stack, tmp_path, "test-next", "Test Next", db_type)

        schema = (tmp_path / "prisma" / "schema.prisma").read_text()

        if db_type == "sqlite":
            assert '"sqlite"' in schema
        else:
            assert f'"{db_type}"' in schema

        assert "model Item" in schema

    @pytest.mark.parametrize("db_type", ["postgresql", "mysql"])
    def test_rust_axum_sqlx_features(self, tmp_path: Path, db_type: str) -> None:
        """Rust-Axum should use the correct SQLx features for each database."""
        stack = get_stack("rust-axum")
        assert stack is not None

        run_stack(stack, tmp_path, "test-axum", "Test Axum", db_type)

        cargo = (tmp_path / "Cargo.toml").read_text()

        if db_type == "postgresql":
            assert '"postgres"' in cargo
        elif db_type == "mysql":
            assert '"mysql"' in cargo

    @pytest.mark.parametrize("db_type", ["postgresql", "mysql", "sqlite"])
    def test_nodejs_fastify_prisma_provider(self, tmp_path: Path, db_type: str) -> None:
        """Fastify Prisma schema should use the correct provider."""
        stack = get_stack("nodejs-fastify")
        assert stack is not None

        run_stack(stack, tmp_path, "test-fastify", "Test Fastify", db_type)

        schema = (tmp_path / "prisma" / "schema.prisma").read_text()

        if db_type == "sqlite":
            assert '"sqlite"' in schema
        else:
            assert f'"{db_type}"' in schema

        assert "model Item" in schema

    @pytest.mark.parametrize("db_type", ["postgresql", "mysql", "sqlite"])
    def test_nodejs_nestjs_prisma_provider(self, tmp_path: Path, db_type: str) -> None:
        """NestJS Prisma schema should use the correct provider."""
        stack = get_stack("nodejs-nestjs")
        assert stack is not None

        run_stack(stack, tmp_path, "test-nest", "Test Nest", db_type)

        schema = (tmp_path / "prisma" / "schema.prisma").read_text()

        if db_type == "sqlite":
            assert '"sqlite"' in schema
        else:
            assert f'"{db_type}"' in schema

        assert "model Item" in schema

    @pytest.mark.parametrize("db_type", ["postgresql", "mysql", "sqlite"])
    def test_nuxt_prisma_provider(self, tmp_path: Path, db_type: str) -> None:
        """Nuxt Prisma schema should use the correct provider."""
        stack = get_stack("nuxt")
        assert stack is not None

        run_stack(stack, tmp_path, "test-nuxt", "Test Nuxt", db_type)

        schema = (tmp_path / "prisma" / "schema.prisma").read_text()

        if db_type == "sqlite":
            assert '"sqlite"' in schema
        else:
            assert f'"{db_type}"' in schema

        assert "model Item" in schema


class TestCleanArchitectureLayers:
    """Verify all functional backend stacks have complete architecture layers."""

    def test_python_fastapi_layers(self, tmp_path: Path) -> None:
        stack = get_stack("python-fastapi")
        assert stack is not None
        run_stack(stack, tmp_path, "test-api", "Test API", "postgresql")

        # Domain
        assert (tmp_path / "src" / "domain" / "entities" / "item.py").is_file()
        assert (tmp_path / "src" / "domain" / "schemas" / "item.py").is_file()
        # Use cases
        assert (tmp_path / "src" / "use_cases" / "item_service.py").is_file()
        # Infrastructure
        assert (tmp_path / "src" / "infrastructure" / "database.py").is_file()
        assert (tmp_path / "src" / "infrastructure" / "repositories" / "item_repository.py").is_file()
        # Controllers
        assert (tmp_path / "src" / "controllers" / "api" / "items.py").is_file()

    def test_nodejs_express_layers(self, tmp_path: Path) -> None:
        stack = get_stack("nodejs-express")
        assert stack is not None
        run_stack(stack, tmp_path, "test-api", "Test API", "postgresql")

        # Domain
        assert (tmp_path / "src" / "domain" / "entities" / "item.ts").is_file()
        assert (tmp_path / "src" / "domain" / "interfaces" / "item-repository.interface.ts").is_file()
        assert (tmp_path / "src" / "domain" / "errors" / "app-error.ts").is_file()
        # Application
        assert (tmp_path / "src" / "application" / "dto" / "item.dto.ts").is_file()
        assert (tmp_path / "src" / "application" / "use-cases" / "item.service.ts").is_file()
        # Infrastructure
        assert (tmp_path / "src" / "infrastructure" / "database" / "prisma-client.ts").is_file()
        assert (tmp_path / "src" / "infrastructure" / "repositories" / "item.repository.ts").is_file()
        # Presentation
        assert (tmp_path / "src" / "presentation" / "routes" / "items.ts").is_file()
        assert (tmp_path / "src" / "presentation" / "controllers" / "item.controller.ts").is_file()
        assert (tmp_path / "src" / "presentation" / "middleware" / "error-handler.ts").is_file()

    def test_react_vite_layers(self, tmp_path: Path) -> None:
        stack = get_stack("react-vite")
        assert stack is not None
        run_stack(stack, tmp_path, "test-app", "Test App")

        # Types
        assert (tmp_path / "src" / "types" / "item.ts").is_file()
        # Services
        assert (tmp_path / "src" / "services" / "api.ts").is_file()
        # Hooks
        assert (tmp_path / "src" / "hooks" / "useItems.ts").is_file()
        assert (tmp_path / "src" / "hooks" / "useApi.ts").is_file()
        # Pages
        assert (tmp_path / "src" / "pages" / "HomePage.tsx").is_file()
        assert (tmp_path / "src" / "pages" / "NotFoundPage.tsx").is_file()
        # Components
        assert (tmp_path / "src" / "components" / "layout" / "AppLayout.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemList.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemCard.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemForm.tsx").is_file()

    def test_python_django_layers(self, tmp_path: Path) -> None:
        """Django uses MVT pattern with DRF ViewSet."""
        stack = get_stack("python-django")
        assert stack is not None
        run_stack(stack, tmp_path, "test-django", "Test Django", "postgresql")

        # Models
        models = tmp_path / "core" / "models.py"
        assert models.is_file()
        assert "class Item" in models.read_text()

        # Serializers
        serializers = tmp_path / "core" / "serializers.py"
        assert serializers.is_file()
        assert "ItemSerializer" in serializers.read_text()

        # Views
        views = tmp_path / "core" / "views.py"
        assert views.is_file()
        assert "ItemViewSet" in views.read_text()

        # URLs with router
        urls = tmp_path / "core" / "urls.py"
        assert urls.is_file()
        urls_content = urls.read_text()
        assert "router" in urls_content
        assert "items" in urls_content

        # Admin
        admin = tmp_path / "core" / "admin.py"
        assert admin.is_file()
        assert "ItemAdmin" in admin.read_text()

        # Config URLs include core
        config_urls = tmp_path / "config" / "urls.py"
        assert config_urls.is_file()
        assert "core.urls" in config_urls.read_text()

        # Tests
        assert (tmp_path / "tests" / "test_items.py").is_file()
        assert "test_create_item" in (tmp_path / "tests" / "test_items.py").read_text()

    def test_python_flask_layers(self, tmp_path: Path) -> None:
        """Flask uses application factory with blueprints."""
        stack = get_stack("python-flask")
        assert stack is not None
        run_stack(stack, tmp_path, "test-flask", "Test Flask", "postgresql")

        # Models
        models = tmp_path / "src" / "models.py"
        assert models.is_file()
        assert "class Item" in models.read_text()

        # Service
        service = tmp_path / "src" / "services" / "item_service.py"
        assert service.is_file()
        assert "class ItemService" in service.read_text()

        # Routes
        routes = tmp_path / "src" / "routes" / "items.py"
        assert routes.is_file()
        routes_content = routes.read_text()
        assert "items_bp" in routes_content
        assert "create_item" in routes_content

        # App registers items blueprint
        app = (tmp_path / "src" / "app.py").read_text()
        assert "items_bp" in app

        # Tests
        assert (tmp_path / "tests" / "test_items.py").is_file()

    def test_nextjs_layers(self, tmp_path: Path) -> None:
        """Next.js uses App Router with API routes."""
        stack = get_stack("nextjs")
        assert stack is not None
        run_stack(stack, tmp_path, "test-next", "Test Next", "postgresql")

        # Types
        types = tmp_path / "src" / "types" / "item.ts"
        assert types.is_file()
        types_content = types.read_text()
        assert "Item" in types_content
        assert "name" in types_content

        # Prisma client singleton
        assert (tmp_path / "src" / "lib" / "db.ts").is_file()

        # API routes
        assert (tmp_path / "src" / "app" / "api" / "items" / "route.ts").is_file()
        assert (tmp_path / "src" / "app" / "api" / "items" / "[id]" / "route.ts").is_file()

        # Items page
        assert (tmp_path / "src" / "app" / "items" / "page.tsx").is_file()

        # Prisma schema
        schema = (tmp_path / "prisma" / "schema.prisma").read_text()
        assert "model Item" in schema
        assert "postgresql" in schema

        # Package.json has prisma
        pkg = (tmp_path / "package.json").read_text()
        assert "@prisma/client" in pkg
        assert "prisma" in pkg

        # Tests
        assert (tmp_path / "tests" / "items.test.ts").is_file()

    def test_rust_axum_layers(self, tmp_path: Path) -> None:
        """Rust-Axum uses clean architecture with Axum + SQLx."""
        stack = get_stack("rust-axum")
        assert stack is not None
        run_stack(stack, tmp_path, "test-axum", "Test Axum", "postgresql")

        # Domain entity
        entity = tmp_path / "src" / "domain" / "entities" / "item.rs"
        assert entity.is_file()
        entity_content = entity.read_text()
        assert "Item" in entity_content
        assert "name" in entity_content

        # Domain errors
        errors = tmp_path / "src" / "domain" / "errors" / "mod.rs"
        assert errors.is_file()
        assert "AppError" in errors.read_text()

        # DTOs
        dto = tmp_path / "src" / "application" / "dto" / "item_dto.rs"
        assert dto.is_file()
        assert "CreateItemDto" in dto.read_text()

        # Service
        service = tmp_path / "src" / "application" / "services" / "item_service.rs"
        assert service.is_file()
        assert "ItemService" in service.read_text()

        # API routes
        routes = tmp_path / "src" / "api" / "routes" / "items.rs"
        assert routes.is_file()
        routes_content = routes.read_text()
        assert "create_item" in routes_content
        assert "list_items" in routes_content

        # Router merges items
        router_mod = (tmp_path / "src" / "api" / "routes" / "mod.rs").read_text()
        assert "items" in router_mod

        # Main uses pool
        main = (tmp_path / "src" / "main.rs").read_text()
        assert "create_pool" in main

        # Cargo.toml has sqlx
        cargo = (tmp_path / "Cargo.toml").read_text()
        assert "sqlx" in cargo
        assert "postgres" in cargo

        # Migration
        assert (tmp_path / "migrations" / "001_create_items.sql").is_file()

        # Integration test
        assert (tmp_path / "tests" / "integration" / "items_test.rs").is_file()

    def test_nodejs_fastify_layers(self, tmp_path: Path) -> None:
        """Fastify uses Prisma + service layer with JSON Schema validation."""
        stack = get_stack("nodejs-fastify")
        assert stack is not None
        run_stack(stack, tmp_path, "test-fastify", "Test Fastify", "postgresql")

        # Domain entity
        assert (tmp_path / "src" / "domain" / "entities" / "item.ts").is_file()
        # Error classes
        assert (tmp_path / "src" / "domain" / "errors" / "app-error.ts").is_file()
        # JSON Schema validation
        assert (tmp_path / "src" / "schemas" / "item.schema.ts").is_file()
        # Service layer
        assert (tmp_path / "src" / "services" / "item.service.ts").is_file()
        # Prisma client
        assert (tmp_path / "src" / "infrastructure" / "prisma-client.ts").is_file()
        # Routes
        assert (tmp_path / "src" / "routes" / "items.ts").is_file()
        # Prisma schema
        schema = (tmp_path / "prisma" / "schema.prisma").read_text()
        assert "model Item" in schema
        # Package deps
        pkg = (tmp_path / "package.json").read_text()
        assert "@prisma/client" in pkg

    def test_nodejs_nestjs_layers(self, tmp_path: Path) -> None:
        """NestJS uses modules with Prisma service and DTOs."""
        stack = get_stack("nodejs-nestjs")
        assert stack is not None
        run_stack(stack, tmp_path, "test-nest", "Test Nest", "postgresql")

        # Prisma module
        assert (tmp_path / "src" / "prisma" / "prisma.service.ts").is_file()
        assert (tmp_path / "src" / "prisma" / "prisma.module.ts").is_file()
        # Items module
        assert (tmp_path / "src" / "items" / "items.module.ts").is_file()
        assert (tmp_path / "src" / "items" / "items.controller.ts").is_file()
        assert (tmp_path / "src" / "items" / "items.service.ts").is_file()
        # DTOs
        assert (tmp_path / "src" / "items" / "dto" / "create-item.dto.ts").is_file()
        assert (tmp_path / "src" / "items" / "dto" / "update-item.dto.ts").is_file()
        # Entity
        assert (tmp_path / "src" / "items" / "entities" / "item.entity.ts").is_file()
        # Exception filter
        assert (tmp_path / "src" / "common" / "filters" / "http-exception.filter.ts").is_file()
        # App module imports items
        app_module = (tmp_path / "src" / "app.module.ts").read_text()
        assert "ItemsModule" in app_module

    def test_php_laravel_layers(self, tmp_path: Path) -> None:
        """Laravel uses Eloquent model with API resource controller."""
        stack = get_stack("php-laravel")
        assert stack is not None
        run_stack(stack, tmp_path, "test-laravel", "Test Laravel", "postgresql")

        # Model
        model = tmp_path / "app" / "Models" / "Item.php"
        assert model.is_file()
        assert "class Item" in model.read_text()
        # Controller
        ctrl = tmp_path / "app" / "Http" / "Controllers" / "ItemController.php"
        assert ctrl.is_file()
        assert "class ItemController" in ctrl.read_text()
        # Form Requests
        assert (tmp_path / "app" / "Http" / "Requests" / "StoreItemRequest.php").is_file()
        assert (tmp_path / "app" / "Http" / "Requests" / "UpdateItemRequest.php").is_file()
        # Migration
        assert (tmp_path / "database" / "migrations" / "0001_01_01_000001_create_items_table.php").is_file()
        # Routes
        api_routes = (tmp_path / "routes" / "api.php").read_text()
        assert "ItemController" in api_routes

    def test_php_symfony_layers(self, tmp_path: Path) -> None:
        """Symfony uses Doctrine entity with route-attribute controller."""
        stack = get_stack("php-symfony")
        assert stack is not None
        run_stack(stack, tmp_path, "test-symfony", "Test Symfony", "postgresql")

        # Entity
        entity = tmp_path / "src" / "Entity" / "Item.php"
        assert entity.is_file()
        assert "class Item" in entity.read_text()
        # Repository
        repo = tmp_path / "src" / "Repository" / "ItemRepository.php"
        assert repo.is_file()
        assert "class ItemRepository" in repo.read_text()
        # Controller
        ctrl = tmp_path / "src" / "Controller" / "ItemController.php"
        assert ctrl.is_file()
        assert "class ItemController" in ctrl.read_text()

    def test_nuxt_layers(self, tmp_path: Path) -> None:
        """Nuxt uses server API routes with Prisma and composables."""
        stack = get_stack("nuxt")
        assert stack is not None
        run_stack(stack, tmp_path, "test-nuxt", "Test Nuxt", "postgresql")

        # Types
        assert (tmp_path / "types" / "item.ts").is_file()
        # Server API routes
        assert (tmp_path / "server" / "api" / "items" / "index.get.ts").is_file()
        assert (tmp_path / "server" / "api" / "items" / "index.post.ts").is_file()
        assert (tmp_path / "server" / "api" / "items" / "[id].get.ts").is_file()
        assert (tmp_path / "server" / "api" / "items" / "[id].patch.ts").is_file()
        assert (tmp_path / "server" / "api" / "items" / "[id].delete.ts").is_file()
        # Prisma client
        assert (tmp_path / "server" / "utils" / "prisma.ts").is_file()
        # Composable
        assert (tmp_path / "composables" / "useItems.ts").is_file()
        # Items page
        assert (tmp_path / "pages" / "items.vue").is_file()
        # Prisma schema
        schema = (tmp_path / "prisma" / "schema.prisma").read_text()
        assert "model Item" in schema

    def test_angular_layers(self, tmp_path: Path) -> None:
        """Angular uses standalone components with HttpClient service."""
        stack = get_stack("angular")
        assert stack is not None
        run_stack(stack, tmp_path, "test-angular", "Test Angular")

        # Model
        assert (tmp_path / "src" / "app" / "models" / "item.model.ts").is_file()
        # Service
        svc = tmp_path / "src" / "app" / "services" / "item.service.ts"
        assert svc.is_file()
        assert "ItemService" in svc.read_text()
        # Components
        assert (tmp_path / "src" / "app" / "components" / "item-card" / "item-card.component.ts").is_file()
        assert (tmp_path / "src" / "app" / "components" / "item-form" / "item-form.component.ts").is_file()
        assert (tmp_path / "src" / "app" / "components" / "item-list" / "item-list.component.ts").is_file()
        # Pages
        assert (tmp_path / "src" / "app" / "pages" / "home" / "home.component.ts").is_file()
        assert (tmp_path / "src" / "app" / "pages" / "not-found" / "not-found.component.ts").is_file()
        # Routes
        routes = (tmp_path / "src" / "app" / "app.routes.ts").read_text()
        assert "HomeComponent" in routes
        assert "NotFoundComponent" in routes
        # Config has HttpClient
        config = (tmp_path / "src" / "app" / "app.config.ts").read_text()
        assert "provideHttpClient" in config

    def test_vue_vite_layers(self, tmp_path: Path) -> None:
        """Vue uses Pinia store with composables and Vue Router."""
        stack = get_stack("vue-vite")
        assert stack is not None
        run_stack(stack, tmp_path, "test-vue", "Test Vue")

        # Types
        assert (tmp_path / "src" / "types" / "item.ts").is_file()
        # Services
        assert (tmp_path / "src" / "services" / "api.ts").is_file()
        # Composables
        assert (tmp_path / "src" / "composables" / "useItems.ts").is_file()
        # Router
        assert (tmp_path / "src" / "router" / "index.ts").is_file()
        # Store
        assert (tmp_path / "src" / "stores" / "items.ts").is_file()
        # Components
        assert (tmp_path / "src" / "components" / "layout" / "AppLayout.vue").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemCard.vue").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemForm.vue").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemList.vue").is_file()
        # Views
        assert (tmp_path / "src" / "views" / "HomeView.vue").is_file()
        assert (tmp_path / "src" / "views" / "NotFoundView.vue").is_file()

    def test_svelte_kit_layers(self, tmp_path: Path) -> None:
        """SvelteKit uses stores with components and file-based routing."""
        stack = get_stack("svelte-kit")
        assert stack is not None
        run_stack(stack, tmp_path, "test-svelte", "Test Svelte")

        # Types
        assert (tmp_path / "src" / "lib" / "types" / "item.ts").is_file()
        # Services
        assert (tmp_path / "src" / "lib" / "services" / "api.ts").is_file()
        # Stores
        assert (tmp_path / "src" / "lib" / "stores" / "items.ts").is_file()
        # Components
        assert (tmp_path / "src" / "lib" / "components" / "ItemCard.svelte").is_file()
        assert (tmp_path / "src" / "lib" / "components" / "ItemForm.svelte").is_file()
        assert (tmp_path / "src" / "lib" / "components" / "ItemList.svelte").is_file()
        # Routes
        assert (tmp_path / "src" / "routes" / "+page.svelte").is_file()
        assert (tmp_path / "src" / "routes" / "+layout.svelte").is_file()
        assert (tmp_path / "src" / "routes" / "+error.svelte").is_file()

    def test_astro_layers(self, tmp_path: Path) -> None:
        """Astro uses Preact islands for interactive CRUD UI."""
        stack = get_stack("astro")
        assert stack is not None
        run_stack(stack, tmp_path, "test-astro", "Test Astro")

        # Types
        assert (tmp_path / "src" / "types" / "item.ts").is_file()
        # Services
        assert (tmp_path / "src" / "services" / "api.ts").is_file()
        # Preact components
        assert (tmp_path / "src" / "components" / "ItemApp.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ItemCard.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ItemForm.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ItemList.tsx").is_file()
        # Pages
        assert (tmp_path / "src" / "pages" / "index.astro").is_file()
        assert (tmp_path / "src" / "pages" / "404.astro").is_file()
        # Layout
        assert (tmp_path / "src" / "layouts" / "Layout.astro").is_file()

    def test_custom_layers(self, tmp_path: Path) -> None:
        """Custom uses pure Python stdlib HTTP server with in-memory CRUD."""
        stack = get_stack("custom")
        assert stack is not None
        run_stack(stack, tmp_path, "test-custom", "Test Custom")

        # Models
        models = tmp_path / "src" / "models.py"
        assert models.is_file()
        models_content = models.read_text()
        assert "class Item" in models_content
        assert "name" in models_content
        assert "description" in models_content

        # Service layer
        service = tmp_path / "src" / "services" / "item_service.py"
        assert service.is_file()
        svc_content = service.read_text()
        assert "class ItemService" in svc_content
        assert "create" in svc_content
        assert "delete" in svc_content

        # HTTP handler
        handlers = tmp_path / "src" / "handlers.py"
        assert handlers.is_file()
        handlers_content = handlers.read_text()
        assert "class ItemHandler" in handlers_content
        assert "do_GET" in handlers_content
        assert "do_POST" in handlers_content

        # Entry point
        main = tmp_path / "src" / "main.py"
        assert main.is_file()
        main_content = main.read_text()
        assert "test-custom" in main_content

        # Config files
        assert (tmp_path / "pyproject.toml").is_file()
        assert (tmp_path / "Makefile").is_file()
        assert (tmp_path / "Dockerfile").is_file()

        # Tests
        assert (tmp_path / "tests" / "test_items.py").is_file()
        test_content = (tmp_path / "tests" / "test_items.py").read_text()
        assert "test_create_item" in test_content

        # No Jinja2 artifacts
        for content in [main_content, models_content, handlers_content]:
            assert "{{" not in content
            assert "{%" not in content


class TestTestFileGeneration:
    """Verify test files are generated for all functional stacks."""

    @pytest.mark.parametrize(
        "stack_id,test_files",
        [
            ("python-fastapi", ["tests/test_items.py", "tests/test_health.py"]),
            ("nodejs-express", ["tests/unit/item.service.test.ts", "tests/integration/items.test.ts"]),
            ("react-vite", ["tests/unit/components/ItemCard.test.tsx", "tests/unit/hooks/useApi.test.ts"]),
            ("python-django", ["tests/test_items.py", "tests/test_health.py"]),
            ("python-flask", ["tests/test_items.py", "tests/test_health.py"]),
            ("nextjs", ["tests/items.test.ts", "tests/health.test.ts"]),
            ("rust-axum", ["tests/integration/items_test.rs"]),
            ("nodejs-fastify", ["tests/items.test.ts", "tests/unit/item.service.test.ts"]),
            ("nodejs-nestjs", ["tests/items.e2e-spec.ts"]),
            ("php-laravel", ["tests/Feature/ItemTest.php"]),
            ("php-symfony", ["tests/Controller/ItemControllerTest.php"]),
            ("nuxt", ["tests/items.test.ts"]),
            (
                "angular",
                ["src/app/services/item.service.spec.ts", "src/app/components/item-card/item-card.component.spec.ts"],
            ),
            ("vue-vite", ["tests/unit/components/ItemCard.test.ts"]),
            ("svelte-kit", ["tests/unit/items.test.ts"]),
            ("astro", ["tests/unit/api.test.ts"]),
            ("custom", ["tests/test_items.py"]),
        ],
    )
    def test_stack_has_test_files(
        self,
        tmp_path: Path,
        stack_id: str,
        test_files: list[str],
    ) -> None:
        stack = get_stack(stack_id)
        assert stack is not None

        db = "postgresql" if stack.requires_database else ""
        run_stack(stack, tmp_path, "test-project", "Test Project", db)

        for test_file in test_files:
            path = tmp_path / test_file
            assert path.is_file(), f"{stack_id}: test file {test_file} missing"
            content = path.read_text()
            assert len(content) > 50, f"{stack_id}: test file {test_file} appears empty"
