import getpass
import sys
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from ...models import Profile
from django.utils.encoding import force_str
from django.utils.text import slugify, capfirst


class Command(BaseCommand):
    help = 'Create User'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.User = get_user_model()
        self.username_field = (self.User._meta.get_field('username'))
        self.email_field = (self.User._meta.get_field('email'))

    def execute(self, *args, **options):
        self.stdin = options.get('stdin', sys.stdin)
        return super().execute(*args, **options)

    def add_arguments(self, parser):
        parser.add_argument('--{0}'.format(self.username_field.name), dest=self.username_field.name, default=None, help='Username')
        parser.add_argument('--{0}'.format(self.email_field.name), dest=self.email_field.name, default=None, help='Email')
        parser.add_argument('--noinput', action='store_false', dest='interactive', default=True, help='Do NOT prompt the user for '
                                                                                                    'input of any kind. You must use '
                                                                                                    '--{} with --noinput, along with '
                                                                                                    'an option for any other '
                                                                                                    'required field. Users created '
                                                                                                    'with --noinput will not be able '
                                                                                                    'to log in until they\'re given '
                                                                                                    'a valid password.'.format(
                                                                                                    self.User.USERNAME_FIELD))
    def clean_value(self, field, value, halt=True):
        try:
            value = field.clean(value, None)
        except ValidationError as e:
            if halt:
                raise CommandError('; '.join(e.messages))
            else:
                sys.stderr.write('Error {0}'.format('; '.join(e.messages)))
        else:
            return value


    def check_unique(self, model, field, value, halt=True):

        q = '{0}__iexact'.format(field.name)
        filt_dict = {q:value}
        obj = model.objects.filter(**filt_dict)
        if not obj:
            return value
        else:
            if halt:
                raise CommandError('That {0} is already taken'.format(capfirst(field.verbose_name)))
            else:
                sys.stderr.write('Error: That {0} is already taken'.format(capfirst(field.verbose_name)))

            return None

    def create_user(self, username, email, password):
        new_user = self.User.objects.create_user(username=username, email=email, password=password)

        try:
            Profile.objects.create(user=new_user, slug=slugify(username))
        except Exception as e:
            raise CommandError('Could not create a Profile:\n'.format('; '.join(e.messages)))

    required_error = ('You must use --{0} with --noinput.')
    def handle_non_interactive(self, username, email, **options):
        if not username:
            raise CommandError(self.required_error.format(self.username_field))

        if not email:
            raise CommandError(self.required_error.format(self.email_field))

        username = self.clean_value(self.username_field, username)
        email = self.clean_value(self.email_field, email)
        username = self.check_unique(self.User, self.username_field, username)
        email = self.check_unique(self.User, self.email_field, email)
        return username, email

    def get_field_interactive(self, model, field):
        value = None
        input_msg = '{0}: '.format(capfirst(field.verbose_name))
        while value is None:
            value = input(input_msg)
            value = self.clean_value(field, value, halt=False)
            if not value:
                continue
            value = self.check_unique(model, field, value, halt=False)
            if not value:
                continue
            return value

    def handle_interactive(self, username, email, **options):
        password = None
        if (hasattr(self.stdin, 'isatty') and not self.stdin.isatty()):
            self.stdout.write('User creation skipped due to not running in a TTY.')
            sys.exit(1)
        if username is not None:
            username = self.clean_value(self.username_field, username, halt=False)
            if username is not None:
                username = self.check_unique(self.User, self.username_field, username)
        if email is not None:
            email = self.clean_value(self.email_field, email, halt=False)
            if username is not None:
                email = self.check_unique(self.User, self.email_field, email)

        try:
            if not username:
                username = self.get_field_interactive(self.User, self.username_field)
            if not email:
                email = self.get_field_interactive(self.User, self.email_field)
            while password is None:
                password = getpass.getpass()
                password2 = getpass.getpass(force_str("Password (again):"))
                if password != password2:
                    sys.stderr.write('Error: passwords didn\'t match')
                    password = None
                    continue
                if password.strip() == '':
                    self.stderr.write('Error: blank passwords not allowed')
                    password = None
                    continue
            return username, email, password
        except KeyboardInterrupt:
            self.stderr.write('\n Operation canceled')
            sys.exit(1)
    def handle(self, **options):
        username = options.pop('username', None)
        email = options.pop('email', None)
        password = None
        if not options['interactive']:
            username, email = (self.handle_non_interactive(username, email, **options))
        else:
            username, email, password = (self.handle_interactive(username, email, **options))

        self.create_user(username, email, password)