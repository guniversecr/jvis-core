"""Tests for jvis.scaffold modules."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

import pytest
import yaml

from jvis.scaffold.docs_structure import create_context_map, create_docs_structure
from jvis.scaffold.framework import install_framework
from jvis.scaffold.monorepo import create_monorepo_root
from jvis.scaffold.shared_files import create_shared_files
from jvis.scaffold.stack_runner import run_stack
from jvis.stacks.registry import get_stack


class TestInstallFramework:
    def test_raises_when_jvis_source_not_found(self, tmp_path):
        """install_framework must raise RuntimeError when .jvis/ source is missing."""
        nonexistent = tmp_path / "nonexistent"
        with (
            patch("jvis.scaffold.framework.get_data_dir", return_value=nonexistent),
            patch("jvis.scaffold.framework.get_repo_root", return_value=nonexistent),
            patch("jvis.scaffold.framework.get_jvis_home", return_value=nonexistent),
            pytest.raises(RuntimeError, match="JVIS framework source"),
        ):
            install_framework(tmp_path / "target")


class TestCreateDocsStructure:
    def test_creates_notes(self, tmp_path):
        create_docs_structure(tmp_path)
        notes = tmp_path / "docs" / "notes"
        assert notes.is_dir()
        assert (notes / "project-log.md").is_file()
        assert (notes / "lessons-learned.md").is_file()
        assert (notes / "next-action.md").is_file()

    def test_creates_agent_notes(self, tmp_path):
        create_docs_structure(tmp_path)
        notes = tmp_path / "docs" / "notes"
        assert (notes / "from-dev.md").is_file()
        assert (notes / "from-qa.md").is_file()
        assert (notes / "from-pm.md").is_file()

    def test_creates_security_dirs(self, tmp_path):
        create_docs_structure(tmp_path)
        sec = tmp_path / "docs" / "security"
        assert sec.is_dir()
        assert (sec / "plans").is_dir()
        assert (sec / "audits").is_dir()
        assert (sec / "threat-models").is_dir()

    def test_creates_other_dirs(self, tmp_path):
        create_docs_structure(tmp_path)
        assert (tmp_path / "docs" / "stories").is_dir()
        assert (tmp_path / "docs" / "qa" / "gates").is_dir()
        assert (tmp_path / "docs" / "architecture").is_dir()


class TestCreateSharedFiles:
    def test_creates_editorconfig(self, tmp_path):
        create_shared_files(tmp_path, "test-project")
        assert (tmp_path / ".editorconfig").is_file()

    def test_creates_readme(self, tmp_path):
        create_shared_files(tmp_path, "test-project", "A test project")
        readme = tmp_path / "README.md"
        assert readme.is_file()
        content = readme.read_text()
        assert "test-project" in content
        assert "A test project" in content

    def test_creates_all_shared_files(self, tmp_path):
        create_shared_files(tmp_path, "test")
        assert (tmp_path / ".env.example").is_file()
        assert (tmp_path / "SECURITY.md").is_file()
        assert (tmp_path / "CONTRIBUTING.md").is_file()
        assert (tmp_path / "CHANGELOG.md").is_file()

    def test_readme_python_stack(self, tmp_path):
        create_shared_files(tmp_path, "test", stack=get_stack("python-fastapi"))
        content = (tmp_path / "README.md").read_text()
        assert "Python 3.12+" in content

    def test_readme_typescript_stack(self, tmp_path):
        create_shared_files(tmp_path, "test", stack=get_stack("react-vite"))
        content = (tmp_path / "README.md").read_text()
        assert "Node.js 20+" in content

    def test_readme_php_stack(self, tmp_path):
        create_shared_files(tmp_path, "test", stack=get_stack("php-laravel"))
        content = (tmp_path / "README.md").read_text()
        assert "PHP 8.3+" in content

    def test_readme_rust_stack(self, tmp_path):
        create_shared_files(tmp_path, "test", stack=get_stack("rust-axum"))
        content = (tmp_path / "README.md").read_text()
        assert "Rust 1.75+" in content


class TestCreateMonorepoRoot:
    def test_creates_directories(self, tmp_path):
        create_monorepo_root(tmp_path, "test", get_stack("python-fastapi"), get_stack("react-vite"))
        assert (tmp_path / "server").is_dir()
        assert (tmp_path / "client").is_dir()

    def test_creates_docker_compose(self, tmp_path):
        create_monorepo_root(tmp_path, "test", get_stack("python-fastapi"), get_stack("react-vite"), "postgresql")
        dc = tmp_path / "docker-compose.yaml"
        assert dc.is_file()
        content = dc.read_text()
        assert "postgres" in content
        assert "server" in content
        assert "client" in content

    def test_creates_makefile(self, tmp_path):
        create_monorepo_root(tmp_path, "test", get_stack("python-fastapi"), get_stack("react-vite"))
        mf = tmp_path / "Makefile"
        assert mf.is_file()
        content = mf.read_text()
        assert "dev-server" in content
        assert "dev-client" in content

    def test_creates_mobile_dir(self, tmp_path):
        create_monorepo_root(
            tmp_path,
            "test",
            get_stack("python-fastapi"),
            get_stack("react-vite"),
            mobile_stack=get_stack("custom"),
        )
        assert (tmp_path / "mobile").is_dir()

    def test_nestjs_backend_port(self, tmp_path):
        create_monorepo_root(tmp_path, "test", get_stack("nodejs-nestjs"), get_stack("react-vite"))
        dc = (tmp_path / "docker-compose.yaml").read_text()
        assert "3001:3001" in dc

    def test_django_backend_cmd(self, tmp_path):
        create_monorepo_root(tmp_path, "test", get_stack("python-django"), get_stack("react-vite"))
        dc = (tmp_path / "docker-compose.yaml").read_text()
        assert "runserver" in dc


class TestStackRunner:
    def test_run_python_fastapi_stack(self, tmp_path):
        stack = get_stack("python-fastapi")
        assert stack is not None
        run_stack(stack, tmp_path, "my-api", "Test API", "postgresql")

        # Check key files were created
        assert (tmp_path / "pyproject.toml").is_file()
        assert (tmp_path / "requirements.txt").is_file()
        assert (tmp_path / "Dockerfile").is_file()
        assert (tmp_path / "src" / "main.py").is_file()

        # Check template rendering
        content = (tmp_path / "pyproject.toml").read_text()
        assert "my-api" in content
        assert "asyncpg" in content  # postgresql driver

    def test_python_fastapi_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold is generated (ADR-002)."""
        stack = get_stack("python-fastapi")
        assert stack is not None
        run_stack(stack, tmp_path, "my-api", "Test API", "postgresql")

        # Database layer
        assert (tmp_path / "src" / "infrastructure" / "database.py").is_file()
        db_content = (tmp_path / "src" / "infrastructure" / "database.py").read_text()
        assert "get_session" in db_content
        assert "create_async_engine" in db_content

        # Domain entity
        assert (tmp_path / "src" / "domain" / "entities" / "base.py").is_file()
        assert (tmp_path / "src" / "domain" / "entities" / "item.py").is_file()
        item_content = (tmp_path / "src" / "domain" / "entities" / "item.py").read_text()
        assert "class Item" in item_content

        # Schemas
        assert (tmp_path / "src" / "domain" / "schemas" / "item.py").is_file()
        schema_content = (tmp_path / "src" / "domain" / "schemas" / "item.py").read_text()
        assert "ItemCreate" in schema_content
        assert "ItemResponse" in schema_content

        # Repository
        repo = tmp_path / "src" / "infrastructure" / "repositories" / "item_repository.py"
        assert repo.is_file()
        assert "class ItemRepository" in repo.read_text()

        # Service
        svc = tmp_path / "src" / "use_cases" / "item_service.py"
        assert svc.is_file()
        assert "class ItemService" in svc.read_text()

        # Controller
        ctrl = tmp_path / "src" / "controllers" / "api" / "items.py"
        assert ctrl.is_file()
        ctrl_content = ctrl.read_text()
        assert "create_item" in ctrl_content
        assert "list_items" in ctrl_content

        # Main registers items router
        main = (tmp_path / "src" / "main.py").read_text()
        assert "items_router" in main

        # Tests
        assert (tmp_path / "tests" / "test_items.py").is_file()
        test_content = (tmp_path / "tests" / "test_items.py").read_text()
        assert "test_create_item" in test_content

        # Alembic
        assert (tmp_path / "alembic" / "env.py").is_file()

        # No Jinja2 artifacts in rendered files
        for f in [main, db_content, ctrl_content]:
            assert "{{" not in f, "Jinja2 artifacts found in rendered file"
            assert "{%" not in f, "Jinja2 artifacts found in rendered file"

    def test_run_react_vite_stack(self, tmp_path):
        stack = get_stack("react-vite")
        assert stack is not None
        run_stack(stack, tmp_path, "my-app", "Test App")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "tsconfig.json").is_file()
        assert (tmp_path / "vite.config.ts").is_file()
        assert (tmp_path / "src" / "App.tsx").is_file()

        content = (tmp_path / "package.json").read_text()
        assert "my-app" in content

    def test_run_nodejs_express_stack(self, tmp_path):
        stack = get_stack("nodejs-express")
        assert stack is not None
        run_stack(stack, tmp_path, "my-service", "Test Service", "postgresql")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "tsconfig.json").is_file()
        assert (tmp_path / "prisma" / "schema.prisma").is_file()

        schema = (tmp_path / "prisma" / "schema.prisma").read_text()
        assert "postgresql" in schema

    def test_nodejs_express_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold is generated (ADR-003)."""
        stack = get_stack("nodejs-express")
        assert stack is not None
        run_stack(stack, tmp_path, "my-service", "Test Service", "postgresql")

        # Domain entity
        entity = tmp_path / "src" / "domain" / "entities" / "item.ts"
        assert entity.is_file()
        entity_content = entity.read_text()
        assert "interface Item" in entity_content
        assert "name" in entity_content
        assert "description" in entity_content

        # Error classes
        errors = tmp_path / "src" / "domain" / "errors" / "app-error.ts"
        assert errors.is_file()
        assert "NotFoundError" in errors.read_text()

        # DTOs
        dto = tmp_path / "src" / "application" / "dto" / "item.dto.ts"
        assert dto.is_file()
        dto_content = dto.read_text()
        assert "CreateItemSchema" in dto_content
        assert "UpdateItemSchema" in dto_content

        # Service
        svc = tmp_path / "src" / "application" / "use-cases" / "item.service.ts"
        assert svc.is_file()
        assert "class ItemService" in svc.read_text()

        # Repository
        repo = tmp_path / "src" / "infrastructure" / "repositories" / "item.repository.ts"
        assert repo.is_file()
        assert "class ItemRepository" in repo.read_text()

        # Prisma client
        assert (tmp_path / "src" / "infrastructure" / "database" / "prisma-client.ts").is_file()

        # Controller (class-based with DI)
        ctrl = tmp_path / "src" / "presentation" / "controllers" / "item.controller.ts"
        assert ctrl.is_file()
        ctrl_content = ctrl.read_text()
        assert "class ItemController" in ctrl_content
        assert "ItemService" in ctrl_content

        # Routes
        routes = tmp_path / "src" / "presentation" / "routes" / "items.ts"
        assert routes.is_file()
        assert "itemsRouter" in routes.read_text()

        # Error handler middleware
        mw = tmp_path / "src" / "presentation" / "middleware" / "error-handler.ts"
        assert mw.is_file()
        assert "errorHandler" in mw.read_text()

        # App registers items router and error handler
        app_content = (tmp_path / "src" / "app.ts").read_text()
        assert "itemsRouter" in app_content
        assert "errorHandler" in app_content

        # Prisma schema has Item model
        schema = (tmp_path / "prisma" / "schema.prisma").read_text()
        assert "model Item" in schema
        assert "postgresql" in schema

        # Tests
        assert (tmp_path / "tests" / "unit" / "item.service.test.ts").is_file()
        test_content = (tmp_path / "tests" / "unit" / "item.service.test.ts").read_text()
        assert "ItemService" in test_content
        assert (tmp_path / "tests" / "integration" / "items.test.ts").is_file()

        # Package.json has supertest
        pkg = (tmp_path / "package.json").read_text()
        assert "supertest" in pkg

        # No Jinja2 artifacts in rendered files
        for content in [app_content, schema, pkg]:
            assert "{{" not in content, "Jinja2 artifacts found in rendered file"
            assert "{%" not in content, "Jinja2 artifacts found in rendered file"

    def test_react_vite_functional_scaffold(self, tmp_path):
        """Verify functional UI scaffold is generated (ADR-003)."""
        stack = get_stack("react-vite")
        assert stack is not None
        run_stack(stack, tmp_path, "my-app", "Test App")

        # App uses React Router
        app_content = (tmp_path / "src" / "App.tsx").read_text()
        assert "Routes" in app_content
        assert "Route" in app_content
        assert "HomePage" in app_content
        assert "NotFoundPage" in app_content

        # Main wraps with BrowserRouter
        main_content = (tmp_path / "src" / "main.tsx").read_text()
        assert "BrowserRouter" in main_content
        assert "index.css" in main_content

        # Types
        types = tmp_path / "src" / "types" / "item.ts"
        assert types.is_file()
        types_content = types.read_text()
        assert "interface Item" in types_content
        assert "name" in types_content
        assert "description" in types_content

        # Services
        api = tmp_path / "src" / "services" / "api.ts"
        assert api.is_file()
        api_content = api.read_text()
        assert "itemsApi" in api_content

        # Config
        config = tmp_path / "src" / "utils" / "config.ts"
        assert config.is_file()
        assert "apiBaseUrl" in config.read_text()

        # Hooks
        assert (tmp_path / "src" / "hooks" / "useApi.ts").is_file()
        assert (tmp_path / "src" / "hooks" / "useItems.ts").is_file()
        assert "useItems" in (tmp_path / "src" / "hooks" / "useItems.ts").read_text()

        # Pages
        assert (tmp_path / "src" / "pages" / "HomePage.tsx").is_file()
        assert (tmp_path / "src" / "pages" / "NotFoundPage.tsx").is_file()

        # Components
        assert (tmp_path / "src" / "components" / "layout" / "AppLayout.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemList.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemCard.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemForm.tsx").is_file()

        # Styles
        assert (tmp_path / "src" / "styles" / "index.css").is_file()

        # Tests
        assert (tmp_path / "tests" / "setup.ts").is_file()
        assert (tmp_path / "tests" / "unit" / "components" / "ItemCard.test.tsx").is_file()
        assert (tmp_path / "tests" / "unit" / "hooks" / "useApi.test.ts").is_file()

        # Package.json has jsdom
        pkg = (tmp_path / "package.json").read_text()
        assert "jsdom" in pkg

        # Vitest config
        vitest = (tmp_path / "vitest.config.ts").read_text()
        assert "jsdom" in vitest

        # No Jinja2 artifacts in rendered files
        for content in [app_content, main_content, api_content, pkg]:
            assert "{{" not in content, "Jinja2 artifacts found in rendered file"
            assert "{%" not in content, "Jinja2 artifacts found in rendered file"

    def test_run_rust_axum_stack(self, tmp_path):
        stack = get_stack("rust-axum")
        assert stack is not None
        run_stack(stack, tmp_path, "my-server", "Test Server", "postgresql")

        assert (tmp_path / "Cargo.toml").is_file()
        assert (tmp_path / "src" / "main.rs").is_file()

        cargo = (tmp_path / "Cargo.toml").read_text()
        assert "my-server" in cargo
        assert "postgres" in cargo

    def test_python_django_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Django (ADR-003)."""
        stack = get_stack("python-django")
        assert stack is not None
        run_stack(stack, tmp_path, "my-django", "Django App", "postgresql")

        # Item model
        models = tmp_path / "core" / "models.py"
        assert models.is_file()
        models_content = models.read_text()
        assert "class Item" in models_content
        assert "name" in models_content
        assert "description" in models_content

        # Serializer
        serializers = tmp_path / "core" / "serializers.py"
        assert serializers.is_file()
        assert "ItemSerializer" in serializers.read_text()

        # ViewSet
        views = tmp_path / "core" / "views.py"
        assert views.is_file()
        views_content = views.read_text()
        assert "ItemViewSet" in views_content
        assert "health_check" in views_content

        # Admin
        admin = tmp_path / "core" / "admin.py"
        assert admin.is_file()
        assert "ItemAdmin" in admin.read_text()

        # URLs with DRF router
        urls = tmp_path / "core" / "urls.py"
        assert urls.is_file()
        urls_content = urls.read_text()
        assert "DefaultRouter" in urls_content
        assert "items" in urls_content

        # Config URLs include core app
        config_urls = (tmp_path / "config" / "urls.py").read_text()
        assert "core.urls" in config_urls

        # Tests
        assert (tmp_path / "tests" / "test_items.py").is_file()
        test_content = (tmp_path / "tests" / "test_items.py").read_text()
        assert "test_create_item" in test_content
        assert "test_list_items" in test_content
        assert "test_delete_item" in test_content

        # No Jinja2 artifacts
        for content in [models_content, views_content, config_urls]:
            assert "{{" not in content
            assert "{%" not in content

    def test_python_flask_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Flask (ADR-003)."""
        stack = get_stack("python-flask")
        assert stack is not None
        run_stack(stack, tmp_path, "my-flask", "Flask App", "postgresql")

        # Item model
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

        # Item routes (blueprint)
        routes = tmp_path / "src" / "routes" / "items.py"
        assert routes.is_file()
        routes_content = routes.read_text()
        assert "items_bp" in routes_content
        assert "create_item" in routes_content
        assert "list_items" in routes_content

        # App registers items blueprint
        app_content = (tmp_path / "src" / "app.py").read_text()
        assert "items_bp" in app_content

        # Tests
        assert (tmp_path / "tests" / "test_items.py").is_file()

        # No Jinja2 artifacts
        for content in [app_content, routes_content]:
            assert "{{" not in content
            assert "{%" not in content

    def test_nextjs_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Next.js (ADR-003)."""
        stack = get_stack("nextjs")
        assert stack is not None
        run_stack(stack, tmp_path, "my-next", "Next App", "postgresql")

        # Types
        types = tmp_path / "src" / "types" / "item.ts"
        assert types.is_file()
        types_content = types.read_text()
        assert "Item" in types_content
        assert "name" in types_content
        assert "description" in types_content

        # Prisma client
        assert (tmp_path / "src" / "lib" / "db.ts").is_file()
        assert "PrismaClient" in (tmp_path / "src" / "lib" / "db.ts").read_text()

        # API routes
        api_items = tmp_path / "src" / "app" / "api" / "items" / "route.ts"
        assert api_items.is_file()
        assert "POST" in api_items.read_text()

        api_item_id = tmp_path / "src" / "app" / "api" / "items" / "[id]" / "route.ts"
        assert api_item_id.is_file()
        id_content = api_item_id.read_text()
        assert "PATCH" in id_content
        assert "DELETE" in id_content

        # Items page
        assert (tmp_path / "src" / "app" / "items" / "page.tsx").is_file()

        # Prisma schema with Item model
        schema = (tmp_path / "prisma" / "schema.prisma").read_text()
        assert "model Item" in schema
        assert "postgresql" in schema

        # Package deps
        pkg = (tmp_path / "package.json").read_text()
        assert "@prisma/client" in pkg

        # Home page links to items
        home = (tmp_path / "src" / "app" / "page.tsx").read_text()
        assert "items" in home.lower()

        # Tests
        assert (tmp_path / "tests" / "items.test.ts").is_file()

        # No Jinja2 artifacts
        for content in [pkg, schema, home]:
            assert "{{" not in content
            assert "{%" not in content

    def test_rust_axum_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Rust-Axum (ADR-003)."""
        stack = get_stack("rust-axum")
        assert stack is not None
        run_stack(stack, tmp_path, "my-axum", "Axum App", "postgresql")

        # Domain entity
        entity = tmp_path / "src" / "domain" / "entities" / "item.rs"
        assert entity.is_file()
        entity_content = entity.read_text()
        assert "Item" in entity_content
        assert "name" in entity_content
        assert "description" in entity_content

        # Domain errors
        errors = tmp_path / "src" / "domain" / "errors" / "mod.rs"
        assert errors.is_file()
        assert "AppError" in errors.read_text()

        # DTOs
        dto = tmp_path / "src" / "application" / "dto" / "item_dto.rs"
        assert dto.is_file()
        dto_content = dto.read_text()
        assert "CreateItemDto" in dto_content
        assert "UpdateItemDto" in dto_content

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
        assert "delete_item" in routes_content

        # Router includes items
        router_mod = (tmp_path / "src" / "api" / "routes" / "mod.rs").read_text()
        assert "items" in router_mod

        # Main uses database pool
        main = (tmp_path / "src" / "main.rs").read_text()
        assert "create_pool" in main
        assert "with_state" in main

        # Database module
        db_mod = (tmp_path / "src" / "infrastructure" / "database" / "mod.rs").read_text()
        assert "DbPool" in db_mod

        # Cargo.toml
        cargo = (tmp_path / "Cargo.toml").read_text()
        assert "sqlx" in cargo
        assert "postgres" in cargo

        # Migration
        migration = tmp_path / "migrations" / "001_create_items.sql"
        assert migration.is_file()
        assert "CREATE TABLE" in migration.read_text()

        # Integration test
        assert (tmp_path / "tests" / "integration" / "items_test.rs").is_file()

        # No Jinja2 artifacts
        for content in [main, cargo, routes_content]:
            assert "{{" not in content
            assert "{%" not in content

    def test_nodejs_fastify_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Fastify (ADR-003)."""
        stack = get_stack("nodejs-fastify")
        assert stack is not None
        run_stack(stack, tmp_path, "my-fastify", "Fastify App", "postgresql")

        # Domain entity
        entity = tmp_path / "src" / "domain" / "entities" / "item.ts"
        assert entity.is_file()
        assert "interface Item" in entity.read_text()

        # Error classes
        assert "NotFoundError" in (tmp_path / "src" / "domain" / "errors" / "app-error.ts").read_text()

        # JSON Schema validation
        assert (tmp_path / "src" / "schemas" / "item.schema.ts").is_file()

        # Service
        svc = tmp_path / "src" / "services" / "item.service.ts"
        assert svc.is_file()
        assert "create" in svc.read_text()

        # Prisma client
        assert (tmp_path / "src" / "infrastructure" / "prisma-client.ts").is_file()

        # Routes
        routes = (tmp_path / "src" / "routes" / "items.ts").read_text()
        assert "items" in routes

        # App registers items routes
        app = (tmp_path / "src" / "app.ts").read_text()
        assert "itemRoutes" in app

        # Prisma schema
        schema = (tmp_path / "prisma" / "schema.prisma").read_text()
        assert "model Item" in schema
        assert "postgresql" in schema

        # Package deps
        pkg = (tmp_path / "package.json").read_text()
        assert "@prisma/client" in pkg

        # Tests
        assert (tmp_path / "tests" / "items.test.ts").is_file()
        assert (tmp_path / "tests" / "unit" / "item.service.test.ts").is_file()

        # No Jinja2 artifacts
        for content in [app, schema, pkg]:
            assert "{{" not in content
            assert "{%" not in content

    def test_nodejs_nestjs_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for NestJS (ADR-003)."""
        stack = get_stack("nodejs-nestjs")
        assert stack is not None
        run_stack(stack, tmp_path, "my-nest", "NestJS App", "postgresql")

        # Prisma module
        assert (tmp_path / "src" / "prisma" / "prisma.service.ts").is_file()
        assert (tmp_path / "src" / "prisma" / "prisma.module.ts").is_file()

        # Items module
        assert (tmp_path / "src" / "items" / "items.module.ts").is_file()
        ctrl = (tmp_path / "src" / "items" / "items.controller.ts").read_text()
        assert "ItemsController" in ctrl
        svc = (tmp_path / "src" / "items" / "items.service.ts").read_text()
        assert "ItemsService" in svc

        # DTOs
        assert (tmp_path / "src" / "items" / "dto" / "create-item.dto.ts").is_file()
        assert (tmp_path / "src" / "items" / "dto" / "update-item.dto.ts").is_file()

        # Entity
        entity = (tmp_path / "src" / "items" / "entities" / "item.entity.ts").read_text()
        assert "Item" in entity
        assert "name" in entity

        # App module imports
        app_module = (tmp_path / "src" / "app.module.ts").read_text()
        assert "ItemsModule" in app_module
        assert "PrismaModule" in app_module

        # Prisma schema
        schema = (tmp_path / "prisma" / "schema.prisma").read_text()
        assert "model Item" in schema

        # Tests
        assert (tmp_path / "tests" / "items.e2e-spec.ts").is_file()

        # No Jinja2 artifacts
        for content in [app_module, schema]:
            assert "{{" not in content
            assert "{%" not in content

    def test_php_laravel_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Laravel (ADR-003)."""
        stack = get_stack("php-laravel")
        assert stack is not None
        run_stack(stack, tmp_path, "my-laravel", "Laravel App", "postgresql")

        # Model
        model = (tmp_path / "app" / "Models" / "Item.php").read_text()
        assert "class Item" in model
        assert "HasUuids" in model

        # Controller
        ctrl = (tmp_path / "app" / "Http" / "Controllers" / "ItemController.php").read_text()
        assert "class ItemController" in ctrl
        assert "index" in ctrl
        assert "store" in ctrl
        assert "destroy" in ctrl

        # Form Requests
        assert (tmp_path / "app" / "Http" / "Requests" / "StoreItemRequest.php").is_file()
        assert (tmp_path / "app" / "Http" / "Requests" / "UpdateItemRequest.php").is_file()

        # Migration
        migration = (tmp_path / "database" / "migrations" / "0001_01_01_000001_create_items_table.php").read_text()
        assert "Schema::create('items'" in migration

        # Routes
        api = (tmp_path / "routes" / "api.php").read_text()
        assert "ItemController" in api

        # Tests
        assert (tmp_path / "tests" / "Feature" / "ItemTest.php").is_file()

    def test_php_symfony_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Symfony (ADR-003)."""
        stack = get_stack("php-symfony")
        assert stack is not None
        run_stack(stack, tmp_path, "my-symfony", "Symfony App", "postgresql")

        # Entity
        entity = (tmp_path / "src" / "Entity" / "Item.php").read_text()
        assert "class Item" in entity
        assert "ORM" in entity

        # Repository
        repo = (tmp_path / "src" / "Repository" / "ItemRepository.php").read_text()
        assert "class ItemRepository" in repo

        # Controller
        ctrl = (tmp_path / "src" / "Controller" / "ItemController.php").read_text()
        assert "class ItemController" in ctrl
        assert "Route" in ctrl

        # Validator config
        assert (tmp_path / "config" / "packages" / "validator.yaml").is_file()

        # Tests
        assert (tmp_path / "tests" / "Controller" / "ItemControllerTest.php").is_file()

    def test_nuxt_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Nuxt (ADR-003)."""
        stack = get_stack("nuxt")
        assert stack is not None
        run_stack(stack, tmp_path, "my-nuxt", "Nuxt App", "postgresql")

        # Types
        types = (tmp_path / "types" / "item.ts").read_text()
        assert "Item" in types
        assert "name" in types

        # Server API routes
        assert (tmp_path / "server" / "api" / "items" / "index.get.ts").is_file()
        assert (tmp_path / "server" / "api" / "items" / "index.post.ts").is_file()
        assert (tmp_path / "server" / "api" / "items" / "[id].get.ts").is_file()
        assert (tmp_path / "server" / "api" / "items" / "[id].patch.ts").is_file()
        assert (tmp_path / "server" / "api" / "items" / "[id].delete.ts").is_file()

        # Prisma
        assert (tmp_path / "server" / "utils" / "prisma.ts").is_file()
        schema = (tmp_path / "prisma" / "schema.prisma").read_text()
        assert "model Item" in schema

        # Composable
        assert (tmp_path / "composables" / "useItems.ts").is_file()

        # Items page
        assert (tmp_path / "pages" / "items.vue").is_file()

        # Home links to items
        home = (tmp_path / "pages" / "index.vue").read_text()
        assert "items" in home.lower()

        # Package deps
        pkg = (tmp_path / "package.json").read_text()
        assert "@prisma/client" in pkg

        # Tests
        assert (tmp_path / "tests" / "items.test.ts").is_file()

    def test_angular_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Angular (ADR-003)."""
        stack = get_stack("angular")
        assert stack is not None
        run_stack(stack, tmp_path, "my-angular", "Angular App")

        # Model
        model = (tmp_path / "src" / "app" / "models" / "item.model.ts").read_text()
        assert "Item" in model
        assert "name" in model

        # Service with HttpClient
        svc = (tmp_path / "src" / "app" / "services" / "item.service.ts").read_text()
        assert "ItemService" in svc
        assert "HttpClient" in svc

        # Components
        assert (tmp_path / "src" / "app" / "components" / "item-card" / "item-card.component.ts").is_file()
        assert (tmp_path / "src" / "app" / "components" / "item-form" / "item-form.component.ts").is_file()
        assert (tmp_path / "src" / "app" / "components" / "item-list" / "item-list.component.ts").is_file()

        # Pages
        assert (tmp_path / "src" / "app" / "pages" / "home" / "home.component.ts").is_file()
        assert (tmp_path / "src" / "app" / "pages" / "not-found" / "not-found.component.ts").is_file()

        # Routes configured
        routes = (tmp_path / "src" / "app" / "app.routes.ts").read_text()
        assert "HomeComponent" in routes

        # Config has HttpClient
        config = (tmp_path / "src" / "app" / "app.config.ts").read_text()
        assert "provideHttpClient" in config

        # App component has RouterLink
        app = (tmp_path / "src" / "app" / "app.component.ts").read_text()
        assert "RouterLink" in app

        # Tests
        assert (tmp_path / "src" / "app" / "services" / "item.service.spec.ts").is_file()
        assert (tmp_path / "src" / "app" / "components" / "item-card" / "item-card.component.spec.ts").is_file()

    def test_vue_vite_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Vue+Vite (ADR-003)."""
        stack = get_stack("vue-vite")
        assert stack is not None
        run_stack(stack, tmp_path, "my-vue", "Vue App")

        # Types
        types = (tmp_path / "src" / "types" / "item.ts").read_text()
        assert "Item" in types
        assert "name" in types

        # Services
        api = (tmp_path / "src" / "services" / "api.ts").read_text()
        assert "itemsApi" in api

        # Composables
        assert (tmp_path / "src" / "composables" / "useItems.ts").is_file()

        # Router
        router = (tmp_path / "src" / "router" / "index.ts").read_text()
        assert "createRouter" in router

        # Pinia store
        assert (tmp_path / "src" / "stores" / "items.ts").is_file()

        # Components
        assert (tmp_path / "src" / "components" / "layout" / "AppLayout.vue").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemCard.vue").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemForm.vue").is_file()
        assert (tmp_path / "src" / "components" / "ui" / "ItemList.vue").is_file()

        # Views
        assert (tmp_path / "src" / "views" / "HomeView.vue").is_file()
        assert (tmp_path / "src" / "views" / "NotFoundView.vue").is_file()

        # Package deps
        pkg = (tmp_path / "package.json").read_text()
        assert "pinia" in pkg
        assert "vue-router" in pkg

        # Main uses pinia and router
        main = (tmp_path / "src" / "main.ts").read_text()
        assert "pinia" in main.lower() or "createPinia" in main
        assert "router" in main.lower()

        # Tests
        assert (tmp_path / "tests" / "unit" / "components" / "ItemCard.test.ts").is_file()

    def test_svelte_kit_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for SvelteKit (ADR-003)."""
        stack = get_stack("svelte-kit")
        assert stack is not None
        run_stack(stack, tmp_path, "my-svelte", "SvelteKit App")

        # Types
        types = (tmp_path / "src" / "lib" / "types" / "item.ts").read_text()
        assert "Item" in types
        assert "name" in types

        # Services
        api = (tmp_path / "src" / "lib" / "services" / "api.ts").read_text()
        assert "itemsApi" in api

        # Stores
        stores = (tmp_path / "src" / "lib" / "stores" / "items.ts").read_text()
        assert "items" in stores
        assert "fetchItems" in stores

        # Components
        assert (tmp_path / "src" / "lib" / "components" / "ItemCard.svelte").is_file()
        assert (tmp_path / "src" / "lib" / "components" / "ItemForm.svelte").is_file()
        assert (tmp_path / "src" / "lib" / "components" / "ItemList.svelte").is_file()

        # Routes
        page = (tmp_path / "src" / "routes" / "+page.svelte").read_text()
        assert "ItemForm" in page or "items" in page.lower()
        layout = (tmp_path / "src" / "routes" / "+layout.svelte").read_text()
        assert "my-svelte" in layout
        assert (tmp_path / "src" / "routes" / "+error.svelte").is_file()

        # Config with project name
        config = (tmp_path / "src" / "lib" / "config.ts").read_text()
        assert "my-svelte" in config

        # Tests
        assert (tmp_path / "tests" / "unit" / "items.test.ts").is_file()

        # No Jinja2 artifacts in key files
        pkg = (tmp_path / "package.json").read_text()
        for content in [pkg, layout, config]:
            assert "{{" not in content
            assert "{%" not in content

    def test_astro_functional_scaffold(self, tmp_path):
        """Verify functional CRUD scaffold for Astro (ADR-003)."""
        stack = get_stack("astro")
        assert stack is not None
        run_stack(stack, tmp_path, "my-astro", "Astro App")

        # Types
        types = (tmp_path / "src" / "types" / "item.ts").read_text()
        assert "Item" in types
        assert "name" in types

        # Services
        api = (tmp_path / "src" / "services" / "api.ts").read_text()
        assert "itemsApi" in api

        # Preact components
        app = (tmp_path / "src" / "components" / "ItemApp.tsx").read_text()
        assert "ItemApp" in app
        assert (tmp_path / "src" / "components" / "ItemCard.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ItemForm.tsx").is_file()
        assert (tmp_path / "src" / "components" / "ItemList.tsx").is_file()

        # Pages
        index = (tmp_path / "src" / "pages" / "index.astro").read_text()
        assert "ItemApp" in index
        assert "client:load" in index
        assert (tmp_path / "src" / "pages" / "404.astro").is_file()

        # Layout has nav
        layout = (tmp_path / "src" / "layouts" / "Layout.astro").read_text()
        assert "my-astro" in layout

        # Astro config has preact
        astro_config = (tmp_path / "astro.config.mjs").read_text()
        assert "preact" in astro_config

        # Package deps
        pkg = (tmp_path / "package.json").read_text()
        assert "@astrojs/preact" in pkg
        assert "preact" in pkg

        # Tests
        assert (tmp_path / "tests" / "unit" / "api.test.ts").is_file()

        # No Jinja2 artifacts in key files
        for content in [pkg, astro_config, layout]:
            assert "{{" not in content
            assert "{%" not in content

    def test_run_custom_stack_generates_crud(self, tmp_path):
        stack = get_stack("custom")
        assert stack is not None
        run_stack(stack, tmp_path, "my-project", "Custom project")

        # Directories
        assert (tmp_path / "src").is_dir()
        assert (tmp_path / "src" / "services").is_dir()
        assert (tmp_path / "tests").is_dir()
        assert (tmp_path / "docs").is_dir()

        # Config files
        assert (tmp_path / "pyproject.toml").is_file()
        assert (tmp_path / "Makefile").is_file()
        assert (tmp_path / "Dockerfile").is_file()

        # Application files
        assert (tmp_path / "src" / "main.py").is_file()
        assert (tmp_path / "src" / "models.py").is_file()
        assert (tmp_path / "src" / "handlers.py").is_file()
        assert (tmp_path / "src" / "services" / "item_service.py").is_file()

        # Tests
        assert (tmp_path / "tests" / "test_items.py").is_file()

        # Template rendering
        content = (tmp_path / "pyproject.toml").read_text()
        assert "my-project" in content
        main_content = (tmp_path / "src" / "main.py").read_text()
        assert "my-project" in main_content

    # --- New stack tests ---

    def test_run_python_django_stack(self, tmp_path):
        stack = get_stack("python-django")
        assert stack is not None
        run_stack(stack, tmp_path, "my-django", "Django App", "postgresql")

        assert (tmp_path / "pyproject.toml").is_file()
        assert (tmp_path / "manage.py").is_file()
        assert (tmp_path / "config" / "settings.py").is_file()
        assert (tmp_path / "config" / "urls.py").is_file()
        assert (tmp_path / "Dockerfile").is_file()

        content = (tmp_path / "pyproject.toml").read_text()
        assert "my-django" in content

    def test_run_python_flask_stack(self, tmp_path):
        stack = get_stack("python-flask")
        assert stack is not None
        run_stack(stack, tmp_path, "my-flask", "Flask App", "postgresql")

        assert (tmp_path / "pyproject.toml").is_file()
        assert (tmp_path / "src" / "app.py").is_file()
        assert (tmp_path / "src" / "routes" / "health.py").is_file()
        assert (tmp_path / "Dockerfile").is_file()

        content = (tmp_path / "pyproject.toml").read_text()
        assert "my-flask" in content

    def test_run_nodejs_nestjs_stack(self, tmp_path):
        stack = get_stack("nodejs-nestjs")
        assert stack is not None
        run_stack(stack, tmp_path, "my-nest", "NestJS App", "postgresql")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "tsconfig.json").is_file()
        assert (tmp_path / "nest-cli.json").is_file()
        assert (tmp_path / "src" / "main.ts").is_file()
        assert (tmp_path / "src" / "app.module.ts").is_file()

        content = (tmp_path / "package.json").read_text()
        assert "my-nest" in content

    def test_run_nodejs_fastify_stack(self, tmp_path):
        stack = get_stack("nodejs-fastify")
        assert stack is not None
        run_stack(stack, tmp_path, "my-fastify", "Fastify App", "postgresql")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "tsconfig.json").is_file()
        assert (tmp_path / "src" / "app.ts").is_file()
        assert (tmp_path / "src" / "routes" / "health.ts").is_file()

        content = (tmp_path / "package.json").read_text()
        assert "my-fastify" in content

    def test_run_php_laravel_stack(self, tmp_path):
        stack = get_stack("php-laravel")
        assert stack is not None
        run_stack(stack, tmp_path, "my-laravel", "Laravel App", "postgresql")

        assert (tmp_path / "composer.json").is_file()
        assert (tmp_path / "artisan").is_file()
        assert (tmp_path / "routes" / "api.php").is_file()
        assert (tmp_path / "app" / "Http" / "Controllers" / "HealthController.php").is_file()

        content = (tmp_path / "composer.json").read_text()
        assert "my-laravel" in content

    def test_run_php_symfony_stack(self, tmp_path):
        stack = get_stack("php-symfony")
        assert stack is not None
        run_stack(stack, tmp_path, "my-symfony", "Symfony App", "postgresql")

        assert (tmp_path / "composer.json").is_file()
        assert (tmp_path / "public" / "index.php").is_file()
        assert (tmp_path / "src" / "Controller" / "HealthController.php").is_file()

        content = (tmp_path / "composer.json").read_text()
        assert "my-symfony" in content

    def test_run_angular_stack(self, tmp_path):
        stack = get_stack("angular")
        assert stack is not None
        run_stack(stack, tmp_path, "my-angular", "Angular App")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "angular.json").is_file()
        assert (tmp_path / "src" / "app" / "app.component.ts").is_file()

        content = (tmp_path / "package.json").read_text()
        assert "my-angular" in content

    def test_run_vue_vite_stack(self, tmp_path):
        stack = get_stack("vue-vite")
        assert stack is not None
        run_stack(stack, tmp_path, "my-vue", "Vue App")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "vite.config.ts").is_file()
        assert (tmp_path / "src" / "App.vue").is_file()

        content = (tmp_path / "package.json").read_text()
        assert "my-vue" in content

    def test_run_svelte_kit_stack(self, tmp_path):
        stack = get_stack("svelte-kit")
        assert stack is not None
        run_stack(stack, tmp_path, "my-svelte", "SvelteKit App")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "svelte.config.js").is_file()
        assert (tmp_path / "src" / "app.html").is_file()

        content = (tmp_path / "package.json").read_text()
        assert "my-svelte" in content

    def test_run_astro_stack(self, tmp_path):
        stack = get_stack("astro")
        assert stack is not None
        run_stack(stack, tmp_path, "my-astro", "Astro Site")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "astro.config.mjs").is_file()
        assert (tmp_path / "src" / "pages" / "index.astro").is_file()

        content = (tmp_path / "package.json").read_text()
        assert "my-astro" in content

    def test_run_nextjs_stack(self, tmp_path):
        stack = get_stack("nextjs")
        assert stack is not None
        run_stack(stack, tmp_path, "my-next", "Next App", "postgresql")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "next.config.ts").is_file()
        assert (tmp_path / "src" / "app" / "layout.tsx").is_file()
        assert (tmp_path / "src" / "app" / "page.tsx").is_file()
        assert (tmp_path / "src" / "app" / "api" / "health" / "route.ts").is_file()

        content = (tmp_path / "package.json").read_text()
        assert "my-next" in content

    def test_run_nuxt_stack(self, tmp_path):
        stack = get_stack("nuxt")
        assert stack is not None
        run_stack(stack, tmp_path, "my-nuxt", "Nuxt App", "postgresql")

        assert (tmp_path / "package.json").is_file()
        assert (tmp_path / "nuxt.config.ts").is_file()
        assert (tmp_path / "app.vue").is_file()
        assert (tmp_path / "server" / "api" / "health.get.ts").is_file()

        content = (tmp_path / "package.json").read_text()
        assert "my-nuxt" in content


class TestCreateContextMap:
    """Tests for context-map.md generation."""

    def test_creates_context_map_file(self, tmp_path):
        (tmp_path / "docs" / "notes").mkdir(parents=True)
        create_context_map(tmp_path, "python-fastapi", "postgresql", "python")
        assert (tmp_path / "docs" / "notes" / "context-map.md").is_file()

    def test_valid_yaml_frontmatter(self, tmp_path):
        (tmp_path / "docs" / "notes").mkdir(parents=True)
        create_context_map(tmp_path, "python-fastapi", "postgresql", "python")
        content = (tmp_path / "docs" / "notes" / "context-map.md").read_text()

        # Extract YAML between --- markers
        parts = content.split("---")
        assert len(parts) >= 3, "Should have YAML front-matter delimiters"
        frontmatter = yaml.safe_load(parts[1])

        assert frontmatter["stack"] == "python-fastapi"
        assert frontmatter["database"] == "postgresql"
        assert frontmatter["primary_language"] == "python"
        assert frontmatter["project_root"] == str(tmp_path)
        assert "last_updated" in frontmatter

    def test_frontmatter_has_all_required_fields(self, tmp_path):
        (tmp_path / "docs" / "notes").mkdir(parents=True)
        create_context_map(tmp_path, "react-vite", "none", "typescript")
        content = (tmp_path / "docs" / "notes" / "context-map.md").read_text()
        parts = content.split("---")
        frontmatter = yaml.safe_load(parts[1])

        required = {"project_root", "main_branch", "remote", "primary_language", "stack", "database", "last_updated"}
        assert required.issubset(frontmatter.keys())

    def test_directory_structure_in_body(self, tmp_path):
        (tmp_path / "docs" / "notes").mkdir(parents=True)
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        create_context_map(tmp_path, "python-fastapi", "postgresql", "python")
        content = (tmp_path / "docs" / "notes" / "context-map.md").read_text()

        assert "src/" in content
        assert "tests/" in content

    def test_hidden_dirs_excluded(self, tmp_path):
        (tmp_path / "docs" / "notes").mkdir(parents=True)
        (tmp_path / ".git").mkdir()
        (tmp_path / ".jvis").mkdir()
        (tmp_path / "src").mkdir()
        create_context_map(tmp_path, "custom", "none", "unknown")
        content = (tmp_path / "docs" / "notes" / "context-map.md").read_text()

        assert ".git" not in content
        assert ".jvis" not in content
        assert "src/" in content

    def test_no_git_repo_uses_defaults(self, tmp_path):
        (tmp_path / "docs" / "notes").mkdir(parents=True)
        create_context_map(tmp_path, "custom", "none", "unknown")
        content = (tmp_path / "docs" / "notes" / "context-map.md").read_text()
        parts = content.split("---")
        frontmatter = yaml.safe_load(parts[1])

        assert frontmatter["main_branch"] == "main"
        assert frontmatter["remote"] == "not configured"

    def test_ssot_no_pyproject_data(self, tmp_path):
        """Context map must NOT contain data that belongs in pyproject.toml."""
        (tmp_path / "docs" / "notes").mkdir(parents=True)
        create_context_map(tmp_path, "python-fastapi", "postgresql", "python")
        content = (tmp_path / "docs" / "notes" / "context-map.md").read_text()
        parts = content.split("---")
        frontmatter = yaml.safe_load(parts[1])

        # These fields belong in pyproject.toml, NOT in context-map
        assert "version" not in frontmatter
        assert "dependencies" not in frontmatter
        assert "name" not in frontmatter  # project name lives in pyproject.toml

    @patch("jvis.scaffold.docs_structure.subprocess.run")
    def test_git_detection_with_valid_repo(self, mock_run, tmp_path):
        """Test that git branch/remote are detected from a real repo."""
        (tmp_path / "docs" / "notes").mkdir(parents=True)

        def side_effect(cmd, **kwargs):
            if "symbolic-ref" in cmd:
                return subprocess.CompletedProcess(cmd, 0, stdout="develop\n", stderr="")
            if "get-url" in cmd:
                return subprocess.CompletedProcess(cmd, 0, stdout="git@github.com:user/repo.git\n", stderr="")
            return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="")

        mock_run.side_effect = side_effect

        create_context_map(tmp_path, "python-fastapi", "postgresql", "python")
        content = (tmp_path / "docs" / "notes" / "context-map.md").read_text()
        parts = content.split("---")
        frontmatter = yaml.safe_load(parts[1])

        assert frontmatter["main_branch"] == "develop"
        assert frontmatter["remote"] == "git@github.com:user/repo.git"

    def test_creates_parent_dirs(self, tmp_path):
        """context-map should create docs/notes/ if it doesn't exist."""
        create_context_map(tmp_path, "custom", "none", "unknown")
        assert (tmp_path / "docs" / "notes" / "context-map.md").is_file()
