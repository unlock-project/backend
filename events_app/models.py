import datetime
import time
from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from polymorphic.models import PolymorphicModel
from users_app.models import Team, User
import secrets


class Event(PolymorphicModel):
    name = models.CharField(max_length=255, null=True, unique=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.date} | {self.name}"


class Attendance(Event):
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.time.strftime('%H:%M')} | {self.name}"

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    pass


class Contest(Event):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contest'
        verbose_name_plural = 'Contests'



class BonusTeam(Event):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Team Bonus'
        verbose_name_plural = 'Team Bonuses'




class BonusUser(Event):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User Bonus'
        verbose_name_plural = 'User Bonuses'




def generate_promo():
    return secrets.token_hex(4).upper()


class Promo(Event):
    CHOICE_LIST = [
        (1, 'User'),
        (2, 'Team'),
    ]
    CONDITION_LIST = [
        (1, 'Active'),
        (2, 'Used'),
    ]
    promo_code = models.CharField(max_length=20, unique=True, default=generate_promo, db_index=True)
    code_type = models.IntegerField(choices=CHOICE_LIST, default=0, verbose_name='Promo type')
    condition = models.IntegerField(choices=CONDITION_LIST, default=0)
    used_by = models.CharField(max_length=100, default=None, blank=True)
    score = models.IntegerField(default=0)
    message = models.TextField(max_length=100, default="Промокод был активирован")
    pass

    def used_message(self):
        return "Промокод не активный"


# Logs
class ContestLog(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, db_index=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} | {self.team} | {self.contest}"


class BonusTeamLog(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, db_index=True, default=None, blank=True, null=True)
    bonus = models.ForeignKey(BonusTeam, on_delete=models.CASCADE, default=True)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Bonus Team Log'
        verbose_name_plural = 'Bonus Team Logs'


class BonusUserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, default=None, blank=True, null=True)
    bonus = models.ForeignKey(BonusUser, on_delete=models.CASCADE, default=True)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Bonus User Log'
        verbose_name_plural = 'Bonus User Logs'


class AttendanceLog(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, default=0)

    def __str__(self):
        return f"{self.id} | {self.user.first_name} {self.user.last_name} | {self.attendance}"

    @property
    def team(self):
        return self.user.team


# Signals
def get_users_by_team_id(team_id):
    users = User.objects.filter(team_id=team_id)
    return users


# Contest

@receiver(pre_delete, sender=ContestLog)
def contest_log_pre_delete(sender, instance, **kwargs):
    instance._original_score = instance.score


@receiver(pre_save, sender=ContestLog)
def contest_log_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = ContestLog.objects.get(pk=instance.pk)
        instance._original_score = old_instance.score
    else:
        instance._original_score = 0


@receiver(post_save, sender=ContestLog)
def contest_log_post_save(sender, instance, **kwargs):
    team = instance.team
    team.balance += instance.score - instance._original_score
    team.save()
    #
    # users = get_users_by_team_id(team.id)
    # for user in users:
    #     user.balance += instance.score - instance._original_score
    #     user.save()


@receiver(post_delete, sender=ContestLog)
def contest_log_post_delete(sender, instance, **kwargs):
    team = instance.team
    team.balance -= instance.score
    team.save()

    # users = get_users_by_team_id(team.id)
    # for user in users:
    #     user.balance -= instance.score
    #     user.save()


# Bonus Team

@receiver(pre_delete, sender=BonusTeamLog)
def bonus_team_log_pre_delete(sender, instance, **kwargs):
    instance._original_score = instance.score


@receiver(pre_save, sender=BonusTeamLog)
def bonus_team_log_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = BonusTeamLog.objects.get(pk=instance.pk)
        instance._original_score = old_instance.score
    else:
        instance._original_score = 0


@receiver(post_save, sender=BonusTeamLog)
def bonus_team_log_post_save(sender, instance, **kwargs):
    team = instance.team
    team.balance += instance.score - instance._original_score
    team.save()

    # users = get_users_by_team_id(team.id)
    # for user in users:
    #     user.balance += instance.score - instance._original_score
    #     user.save()


@receiver(post_delete, sender=BonusTeamLog)
def bonus_team_log_post_delete(sender, instance, **kwargs):
    team = instance.team
    team.balance -= instance.score
    team.save()

    # users = get_users_by_team_id(team.id)
    # for user in users:
    #     user.balance -= instance.score
    #     user.save()


# Bonus User
@receiver(pre_delete, sender=BonusUserLog)
def bonus_user_log_pre_delete(sender, instance, **kwargs):
    user = instance.user
    user.balance -= instance.score
    team = user.team
    team.balance -= instance.score


@receiver(pre_save, sender=BonusUserLog)
def bonus_user_log_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = BonusUserLog.objects.get(pk=instance.pk)
        instance._original_score = old_instance.score
    else:
        instance._original_score = 0
    user = instance.user
    user.balance += instance.score - instance._original_score
    team = user.team
    team.balance += instance.score - instance._original_score
    team.save()


@receiver(post_save, sender=BonusUserLog)
def bonus_user_log_post_save(sender, instance, **kwargs):
    user = instance.user
    user.save()
    team = user.team
    team.save()


@receiver(post_delete, sender=BonusUserLog)
def bonus_user_log_post_save(sender, instance, **kwargs):
    user = instance.user
    user.save()
    team = user.team
    team.save()


# Promo
def check_and_apply_promo_code(user_id, promo_code):
    try:
        entry_promo = Promo.objects.get(promo_code=promo_code, condition=1)
    except Promo.DoesNotExist:
        return "Промокод не найден или уже использован."

    user = User.objects.get(id=user_id)

    if entry_promo.code_type == 1:
        entry_promo.used_by = f"{user.first_name} {user.last_name}"
        user.balance += entry_promo.score
        user.save()
    elif entry_promo.code_type == 2:
        team = user.team
        entry_promo.used_by = f"{team.name}, {user.first_name} {user.last_name}"
        team.balance += entry_promo.score
        # users = User.objects.filter(team_id=user.team_id)
        # for user_ in users:
        #     user_.balance += entry_promo.score
        #     user_.save()
        team.save()

    entry_promo.condition = 2
    entry_promo.save()

    return "Промокод успешно активирован!"


# Attendance
def mark_attendance(user_id, attendance_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return "Пользователь с указанным id не найден."

    try:
        attendance = Attendance.objects.get(id=attendance_id)
    except Attendance.DoesNotExist:
        return "Событие посещаемости с указанным id не найдено."

    if AttendanceLog.objects.filter(user=user, attendance=attendance).exists():
        return "Вы уже отметились на это событие."

    attendance_log = AttendanceLog.objects.create(user=user, attendance=attendance)
    attendance_log.save()

    user.balance += attendance.score
    user.team.balance += attendance.score
    user.save()

    return f"Посещаемость отмечена успешно!"


@receiver(post_save, sender=AttendanceLog)
def attendance_log_post_save(sender, instance, **kwargs):
    user = instance.user
    attendance = Attendance.objects.get(id=instance.attendance.id)
    user.balance += attendance.score
    if user.team is not None:
        team = user.team
        users = User.objects.filter(team=team)
        team.balance += attendance.score * 10 / len(users)
        team.save()
    user.save()
