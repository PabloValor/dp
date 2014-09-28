# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task

from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_email(email_template, subject, to_email, template_data):
    plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext

    text_body = render_to_string("notifications/{0}.txt".format(email_template), template_data, plaintext_context)
    html_body = render_to_string("notifications/{0}.html".format(email_template), template_data )

    msg = EmailMultiAlternatives(subject=subject, from_email="equipo@dpfutbol.com",
                                to=[to_email], body=text_body)
    msg.attach_alternative(html_body, "text/html")
    msg.send()

@shared_task
def send_friend_notification_email(to_email, from_username):
    send_email('email_friend_invitation', 
               u'Notificatión de DP Futbol: te enviaron un pedido de amistad.', 
               to_email, { 'sender': from_username})

@shared_task
def send_game_notification_email(to_email, from_username, game_name):
    send_email('email_game_invitation', u'Notificación de DP Futbol: te invitaron a un torneo.', 
              to_email, { 'sender': from_username, 'game_name': game_name })

@shared_task
def send_welcome_email(player):
    send_email('email_welcome', 'Bienvenido a DP futbol', player['email'], {})
