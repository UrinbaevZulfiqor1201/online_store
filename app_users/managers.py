from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email: str,
                    first_name: str = "",
                    last_name: str = "",
                    password: str = None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str,
                         first_name: str,
                         last_name: str,
                         password: str):
        superuser = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser

