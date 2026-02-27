"""Tests for jvis.stacks.registry."""

from __future__ import annotations

from jvis.stacks.registry import discover_stacks, get_stack, get_stacks_by_type


class TestDiscoverStacks:
    def test_discovers_stacks(self):
        stacks = discover_stacks()
        assert len(stacks) >= 16
        assert "custom" in stacks
        assert "python-fastapi" in stacks
        assert "react-vite" in stacks
        assert "nodejs-express" in stacks
        assert "rust-axum" in stacks

    def test_discovers_new_backend_stacks(self):
        stacks = discover_stacks()
        assert "python-django" in stacks
        assert "python-flask" in stacks
        assert "nodejs-nestjs" in stacks
        assert "nodejs-fastify" in stacks
        assert "php-laravel" in stacks
        assert "php-symfony" in stacks

    def test_discovers_new_frontend_stacks(self):
        stacks = discover_stacks()
        assert "angular" in stacks
        assert "vue-vite" in stacks
        assert "svelte-kit" in stacks
        assert "astro" in stacks

    def test_discovers_fullstack_stacks(self):
        stacks = discover_stacks()
        assert "nextjs" in stacks
        assert "nuxt" in stacks
        nextjs = stacks["nextjs"]
        assert nextjs.type == "fullstack"
        nuxt = stacks["nuxt"]
        assert nuxt.type == "fullstack"

    def test_stack_has_required_fields(self):
        stacks = discover_stacks()
        for stack_id, info in stacks.items():
            assert info.id == stack_id
            assert info.name
            assert info.directory.is_dir()


class TestGetStacksByType:
    def test_backend_stacks(self):
        backends = get_stacks_by_type("backend")
        assert "python-fastapi" in backends
        assert "python-django" in backends
        assert "python-flask" in backends
        assert "nodejs-express" in backends
        assert "nodejs-nestjs" in backends
        assert "nodejs-fastify" in backends
        assert "php-laravel" in backends
        assert "php-symfony" in backends
        assert "rust-axum" in backends
        assert "react-vite" not in backends

    def test_frontend_stacks(self):
        frontends = get_stacks_by_type("frontend")
        assert "react-vite" in frontends
        assert "angular" in frontends
        assert "vue-vite" in frontends
        assert "svelte-kit" in frontends
        assert "astro" in frontends
        assert "python-fastapi" not in frontends

    def test_fullstack_stacks(self):
        fullstack = get_stacks_by_type("fullstack")
        assert "nextjs" in fullstack
        assert "nuxt" in fullstack
        assert "python-fastapi" not in fullstack

    def test_empty_type(self):
        result = get_stacks_by_type("nonexistent")
        assert len(result) == 0


class TestGetStack:
    def test_existing_stack(self):
        stack = get_stack("python-fastapi")
        assert stack is not None
        assert stack.name == "Python FastAPI + Clean Architecture"
        assert stack.type == "backend"
        assert stack.language == "python"
        assert stack.requires_database is True

    def test_new_python_django_stack(self):
        stack = get_stack("python-django")
        assert stack is not None
        assert stack.type == "backend"
        assert stack.language == "python"
        assert stack.framework == "django"
        assert stack.requires_database is True

    def test_new_php_laravel_stack(self):
        stack = get_stack("php-laravel")
        assert stack is not None
        assert stack.type == "backend"
        assert stack.language == "php"
        assert stack.framework == "laravel"

    def test_new_angular_stack(self):
        stack = get_stack("angular")
        assert stack is not None
        assert stack.type == "frontend"
        assert stack.language == "typescript"
        assert stack.requires_database is False

    def test_new_nextjs_stack(self):
        stack = get_stack("nextjs")
        assert stack is not None
        assert stack.type == "fullstack"
        assert stack.language == "typescript"
        assert stack.framework == "nextjs"

    def test_missing_stack(self):
        assert get_stack("nonexistent") is None
