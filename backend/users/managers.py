from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """Custon user manager for project."""

    def create_user(
            self,
            email,
            password=None,
    ):
        """Create user."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email,
            password=None,
    ):
        """Create supuser."""
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
