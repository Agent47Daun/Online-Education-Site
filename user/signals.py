from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User, StudentAccount, TeacherAccount


@receiver(post_save, sender=User)
def create_and_save_additional_accounts(sender, instance, created, **kwargs):
    if created:
        if instance.account_type == 0:
            student_account = StudentAccount.objects.create()
            instance.student_account = student_account
            instance.student_account.save()

        else:
            teacher_account = TeacherAccount.objects.create()
            instance.teacher_account = teacher_account
            instance.teacher_account.save()
