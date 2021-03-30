from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
import datetime
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
       
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()



#end of model manager of custom user















class User(AbstractBaseUser, PermissionsMixin):





    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
  
    first_name=models.CharField(_('first_name'),max_length=25,blank=False,null=False)
    last_name=models.CharField(_('last_name'),max_length=25,blank=False,null=False)
    email = models.EmailField(_('email address'), blank=False,unique=True)
    mobile=PhoneNumberField(blank=False,null=False,max_length=16)
    address=models.CharField(_('address'),max_length=45,blank=False,null=False)
    country = CountryField(blank=False,null=False,blank_label='(select country)')

    company=models.CharField(_('company'),max_length=50,blank=True,null=True)
    is_agent=models.BooleanField(_('is_agent'),default=False)
    agent_id=models.IntegerField(default=0)
    profile_picture=models.ImageField(upload_to='profile/',blank=True,null=True)
    nid_front=models.ImageField(upload_to='nid/',blank=True,null=True)
    nid_back=models.ImageField(upload_to='nid/',blank=True,null=True)
    
    
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','mobile','address','country']

    class Meta:
        verbose_name = _('users')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'


   

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name,self.last_name)
        return first_name+''+last_name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)








