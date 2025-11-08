import pytest
from unittest.mock import patch, MagicMock
from resources.container import Container, bootstrap


@pytest.fixture
def mocked_services():
    """Patch all real service constructors to avoid network/disk use."""
    with (
        patch(
            "service.cacheService.CacheService",
            return_value=MagicMock(name="CacheService"),
        ),
        patch(
            "service.emailService.EmailService",
            return_value=MagicMock(name="EmailService"),
        ),
        patch(
            "service.fileService.FileService",
            return_value=MagicMock(name="FileService"),
        ),
        patch(
            "service.tokenService.TokenService",
            return_value=MagicMock(name="TokenService"),
        ),
        patch(
            "service.authService.AuthService",
            return_value=MagicMock(name="AuthService"),
        ),
        patch(
            "service.userService.UserService",
            return_value=MagicMock(name="UserService"),
        ),
        patch(
            "controller.authController.AuthController",
            return_value=MagicMock(name="AuthController"),
        ),
        patch(
            "controller.userController.UserController",
            return_value=MagicMock(name="UserController"),
        ),
        patch(
            "controller.fileController.FileController",
            return_value=MagicMock(name="FileController"),
        ),
    ):
        yield


def test_bootstrap_creates_container(mocked_services):
    """Ensure bootstrap initializes container successfully."""
    container = bootstrap()
    assert isinstance(container, Container)


def test_resolve_registered_services(mocked_services):
    """Verify all registered services and controllers can be resolved properly."""
    c = bootstrap()

    cache = c.resolve("CacheService")
    email = c.resolve("EmailService")
    file = c.resolve("FileService")
    token = c.resolve("TokenService")

    auth_service = c.resolve("AuthService")
    user_service = c.resolve("UserService")
    with c.create_scope() as scope:
        auth_controller = c.resolve("AuthController", scope=scope)
        user_controller = c.resolve("UserController", scope=scope)
        file_controller = c.resolve("FileController", scope=scope)

        assert auth_controller
        assert user_controller
        assert file_controller

    assert cache and email and file and token and auth_service and user_service


def test_singleton_and_transient_lifetimes(mocked_services):
    """Singletons should be identical; transients should differ."""
    c = bootstrap()

    s1 = c.resolve("CacheService")
    s2 = c.resolve("CacheService")
    assert s1 is s2, "Singletons should return the same instance"

    t1 = c.resolve("TokenService")
    t2 = c.resolve("TokenService")
    assert t1 is not t2, "Transients should return different instances"
