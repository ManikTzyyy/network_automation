from django.db import models

class Device(models.Model):
    # membuat field
    ip_address = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    CONFIG_CHOICES = [
        ('simple_queue', 'Simple Queue'),
        ('queue_three', 'Queue Three'),
        ('HTB', 'HTB'),
    ]

    config = models.CharField(max_length=255, choices=CONFIG_CHOICES, default='default')


    # membuat pilihan
    # VENDOR_CHOICES = [
    #     ('Mikrotik', 'Mikrotik'),
    #     ('Cisco', 'Cisco')
    # ]

    # membuat field berdasarkan pilihan
    # vendor = models.CharField(max_length=225, choices=VENDOR_CHOICES)

    def __str__(self):
        return "{} - {}".format(self.hostname, self.ip_address)
