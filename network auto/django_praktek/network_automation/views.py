from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
# Create your views here.

import paramiko, time

from .models import Device

from django.contrib import messages

import ipaddress 


def devices(request):
    all_devices = Device.objects.all()
    devices = Device.objects.all()



    context = {
        'title' : "Devices",
        'active_devices' : 'active',
        'devices' : devices,
        'all_devices' : len(all_devices),
    }
    return render(request, 'devices.html', context)

def main(request):
    all_devices = Device.objects.all()

    devices = Device.objects.all()



    context = {
        'title' : "Devices",
        'active_devices' : 'active',
        'devices' : devices,
        'all_devices' : len(all_devices),
    }
    return render(request, 'main.html', context)


# def config(request):
#     return HttpResponse("hello world"),



# create
def addpage(request):
    if request.method == "POST":
        hostname = request.POST.get('hostname')
        ip_address = request.POST.get('ip_address')
        username = request.POST.get('username')
        password = request.POST.get('password_device')
        


        if hostname == "" or ip_address == "" or username == "" :
            messages.error(request, "All fields must be filled")
            return redirect('devices')

        # insert data to database
        add_device = Device(hostname=hostname, ip_address=ip_address, username=username, password=password)
        add_device.save()

        # success message
        messages.success(request, "Successfully added device")
        return redirect('devices')
    
    else:
        messages.error(request, "Failed to add device")
        
    context = {
        'title' : "Add",
        'active_devices' : 'active',
    }
    return render(request, 'addpage.html', context)
# end create

# delete
def delete_device(request, id_device):
    # data by id
    device = Device.objects.get(id=id_device)

    # delete data in the database
    device.delete()


    # success message
    messages.success(request, "Successfully deleted device")
    return redirect('devices')
# end delete

def config(request, id_device):
    device = get_object_or_404(Device, id=id_device)

    if request.method == "POST":
        hostname = request.POST.get('edit_hostname')
        ip_address = request.POST.get('edit_ip_address')
        username = request.POST.get('edit_username')
        password = request.POST.get('edit_password_device')
        # Update data in the database
        device.hostname = hostname
        device.ip_address = ip_address
        device.username = username
        device.password = password

        device.save()
        # Success message
        messages.success(request, "Successfully edited device")
        return redirect('devices')
    # Failure message
    messages.error(request, "Failed to edit device")
    
    context = {
        'title' : "Edit Config",
        'active_devices' : 'active',
        'device' : device
    }

    return render(request, 'config.html', context)

def simple_queue(request, id_device):
    device = get_object_or_404(Device, id=id_device)

    if request.method == 'POST':
        config = request.POST.get('config')

        if config == 'simple_queue':
            ip_target = request.POST.get('target_simple_queue')
            simple_que_max_down = request.POST.get('simple_que_max_down')
            simple_que_max_up = request.POST.get('simple_que_max_up')

            # Validate IP address
            try:
                set_bandwidth_via_cli(device.id, device.ip_address, device.username, device.password, ip_target, simple_que_max_down, simple_que_max_up)
            except ValueError as ve:
                messages.error(request, f"Invalid IP address: {ve}")
            except Exception as e:
                messages.error(request, f"Failed to set bandwidth: {e}")

        elif config == 'queue_three':
        
            Qtree_ip_target = request.POST.get('target_queue_three')
            try:
                queue_tree(device.id, device.ip_address, device.username, device.password, Qtree_ip_target,)
            except ValueError as ve:
                messages.error(request, f"Invalid IP address: {ve}")
            except Exception as e:
                messages.error(request, f"Failed to set bandwidth: {e}")

        elif config == 'HTB':
        
            ip_htb = request.POST.get('target_htb')
            condition = request.POST.get('condition')
            try:
                htb(device.id, device.ip_address, device.username, device.password, ip_htb,condition)
            except ValueError as ve:
                messages.error(request, f"Invalid IP address: {ve}")
            except Exception as e:
                messages.error(request, f"Failed to set bandwidth: {e}")

        elif config == 'Qt_upload':
        
            Qtree_ip_target = request.POST.get('Qt_upload')
            try:
                Qt_upload(device.id, device.ip_address, device.username, device.password, Qtree_ip_target,)
            except ValueError as ve:
                messages.error(request, f"Invalid IP address: {ve}")
            except Exception as e:
                messages.error(request, f"Failed to set bandwidth: {e}")

        elif config == 'Qtree_setDown':
        
            qtreedownload = request.POST.get('qtreeSetdown')
            try:
                qtdown(device.id, device.ip_address, device.username, device.password, qtreedownload)
            except ValueError as ve:
                messages.error(request, f"Invalid IP address: {ve}")
            except Exception as e:
                messages.error(request, f"Failed to set bandwidth: {e}")

        elif config == 'Qtree_setUplod':
        
            Qtree_setUplod = request.POST.get('qtreeSetUP')
            try:
                Qtree_setUp(device.id, device.ip_address, device.username, device.password, Qtree_setUplod,)
            except ValueError as ve:
                messages.error(request, f"Invalid IP address: {ve}")
            except Exception as e:
                messages.error(request, f"Failed to set bandwidth: {e}")

        else:
            messages.error(request, "Invalid configuration type")

        device.config = config
        device.save()

        context = {
            'title': "Simple Queue",
            'active_devices': 'active',
            'device': device
        }
        return render(request, 'config.html', context)
    else:
        return HttpResponse("Invalid request method")

# simple queue function
def set_bandwidth_via_cli(id_device, ip_address, username, password, ip_target, simple_que_max_down, simple_que_max_up):
    device = get_object_or_404(Device, id=id_device)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(hostname=ip_address, username=username, password=password)

        command = f'/queue simple add target={ip_target} max-limit={simple_que_max_down}/{simple_que_max_up}'
        stdin, stdout, stderr = ssh.exec_command(command)

        # Handle the command output as needed

    except paramiko.AuthenticationException:
        raise Exception("Authentication failed.")

    except paramiko.SSHException as e:
        raise Exception(f"SSH error: {e}")

    except Exception as e:
        raise Exception(f"Error: {e}")

    finally:
        ssh.close()



# queue tree function
def queue_tree(id_device, ip_address, username, password, Qtree_ip_target):
    device = get_object_or_404(Device, id=id_device)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(hostname=ip_address, username=username, password=password)
        command = f'/ip firewall address-list add address={Qtree_ip_target} list=download-src'
        stdin, stdout, stderr = ssh.exec_command(command)

    except paramiko.AuthenticationException:
        raise Exception("Authentication failed.")

    except paramiko.SSHException as e:
        raise Exception(f"SSH error: {e}")

    except Exception as e:
        raise Exception(f"Error: {e}")

    finally:
        ssh.close()
# htb 
def htb(id_device, ip_address, username, password, ip_htb, condition):
    device = get_object_or_404(Device, id=id_device)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(hostname=ip_address, username=username, password=password)
        command = f'/ip firewall address-list add address={ip_htb} list={condition}-htb'
        stdin, stdout, stderr = ssh.exec_command(command)

    

    except paramiko.AuthenticationException:
        raise Exception("Authentication failed.")

    except paramiko.SSHException as e:
        raise Exception(f"SSH error: {e}")

    except Exception as e:
        raise Exception(f"Error: {e}")

    finally:
        ssh.close()

def Qt_upload(id_device, ip_address, username, password, Qtree_ip_target):
    device = get_object_or_404(Device, id=id_device)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(hostname=ip_address, username=username, password=password)
        command = f'/ip firewall address-list add address={Qtree_ip_target} list=upload-dst'
        stdin, stdout, stderr = ssh.exec_command(command)

    

    except paramiko.AuthenticationException:
        raise Exception("Authentication failed.")

    except paramiko.SSHException as e:
        raise Exception(f"SSH error: {e}")

    except Exception as e:
        raise Exception(f"Error: {e}")

    finally:
        ssh.close()


def qtdown(id_device, ip_address, username, password, qtreedownload):
    
    device = get_object_or_404(Device, id=id_device)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(hostname=ip_address, username=username, password=password)
        
        command = f'/queue tree set download-parent max-limit={qtreedownload}'
        stdin, stdout, stderr = ssh.exec_command(command)


    except paramiko.AuthenticationException:
        raise Exception("Authentication failed.")

    except paramiko.SSHException as e:
        raise Exception(f"SSH error: {e}")

    except Exception as e:
        raise Exception(f"Error: {e}")

    finally:
        ssh.close()

def Qtree_setUp(id_device, ip_address, username, password, Qtree_setUplod):

    device = get_object_or_404(Device, id=id_device)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(hostname=ip_address, username=username, password=password)

        command = f'/queue tree set upload-parent max-limit={Qtree_setUplod}'
        stdin, stdout, stderr = ssh.exec_command(command)

    except paramiko.AuthenticationException:
        raise Exception("Authentication failed.")

    except paramiko.SSHException as e:
        raise Exception(f"SSH error: {e}")

    except Exception as e:
        raise Exception(f"Error: {e}")

    finally:
        ssh.close()


def edit_device(request, id_device):

    # data by id
    device = Device.objects.get(id=id_device)
    
    if request.method == "POST":
        hostname = request.POST.get('edit_hostname')
        ip_address = request.POST.get('edit_ip_address')
        username = request.POST.get('edit_username')
        password = request.POST.get('edit_password_device')
     

        # Update data in the database
        device.hostname = hostname
        device.ip_address = ip_address
        device.username = username
        device.password = password
     
        device.save()

        # success message
        messages.success(request, "Successfully edited device")

        return redirect('devices')
    else:
        messages.error(request, "Failed to edit device")
        
    context = {
        'title' : "Edit Devices",
        'active_devices' : 'active',
        'device' : device
    }

    return render(request, 'edit_devices.html', context)
# end edit


def ping(request, id_device):
    device = get_object_or_404(Device, id=id_device)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        # Establish SSH connection
        ssh.connect(hostname=device.ip_address, username=device.username, password=device.password)

        # Execute ping command
        ping_command = f"/ping {device.ip_address} count=3"
        stdin, stdout, stderr = ssh.exec_command(ping_command)

        # Read the output
        output = stdout.read()
    except Exception as e:
        # Handle exceptions (e.g., SSH connection error)
        output = f"Error: {str(e)}"
    finally:
        # Close the SSH connection
        ssh.close()

    return HttpResponse(output)


# def ping(request):
#     ssh= paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# # buat connet ke mikro
#     ssh.connect(hostname="192.168.1.128", username="admin", password="")

# #buat terminal
#     stdin, stdout, stderr = ssh.exec_command("/ping 192.168.1.128 count=3")

#     output = stdout.read()

#     ssh.close
#     return HttpResponse(output)


# def reboot(request):
#     ssh= paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# # buat connet ke mikro
#     ssh.connect(hostname="192.168.1.128", username="admin", password="")

# #buat terminal
#     stdin, stdout, stderr = ssh.exec_command("/system reboot")

#     output = stdout.read()

#     ssh.close
#     return redirect()
