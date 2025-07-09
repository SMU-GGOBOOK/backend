from django.shortcuts import render

def main(request):
    return render(request,'shareReading/Share_Main.html')

def addgroup(request):
    return render(request,'shareReading/Share_Addgroup.html')