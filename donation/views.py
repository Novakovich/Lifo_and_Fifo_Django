from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
import json

def home_page(request):
     return HttpResponse(
         '''
            <!DOCTYPE html>
            <html>
            <head>
                <!-- CSS only -->
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
            </head>
            <body>
                <div style="position: relative; padding: 10px; ">
                    <div class="card" style="width: 26rem;">
                        <div class="card-header">
                            <h3>Donation Form</h3>
                        </div>
                        <div class="card-body">
                            <form action="/donate" method="post">
                                <div class="registation">
                                    <label>Name
                                        <input type="text" name="name" class="form-control">
                                    </label>
                                    <div id="name" class="form-text">Enter thing's name.</div>
                                </div>
                                <p>
                                </p>
                                <label>Amount
                                    <input type="number" name="amount" class="form-control">
                                </label>
                                <div id="amount" class="form-text">Enter amount of things.</div>
                                 <p>
                                </p>
                                <button type="submit" class="btn btn-primary" style="width: 24rem;">Donate</button>
                            </form>
                        </div>
                    </div>
                </div>
                <div style="position: relative; padding: 10px;">
                    <div class="card" style="width: 26rem;">
                        <div class="card-header">
                            <h3>Registration Donating</h3>
                        </div>
                        <div class="card-body">
                            <form action="/request/donation">
                                <button type="submit" class="btn btn-primary" style="width: 24rem;" >Ask for donate</button>
                            </form>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        '''
     )

def donate(request):
    with open('datajson.json', 'r', encoding='utf-8') as data:
        data_list = json.load(data)
        data_list.append(
            {"name": request.POST["name"], "amount": request.POST["amount"]}
        )
    with open('datajson.json', 'w') as data:
        json.dump(data_list, data)
    return HttpResponse(
            '''
                <!DOCTYPE html>
                <html>
                <head>
                    <!-- CSS only -->
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
                </head>
                <body>
                    <h5>Thank you</h5>
                    <p>
                    <a href="/">Return main</a>
                    </p>
                </body>
                </html>
            '''
        )

def donation(request):
    with open('datajson.json', 'r', encoding='utf-8') as data:
        data_list = json.load(data)
    if not data_list:
        return HttpResponse(
            '''
                <!DOCTYPE html>
                <html>
                <head>
                    <!-- CSS only -->
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
                </head>
                <body>
                    <h5>We have nothing for you</h5>
                    <p>
                    <a href="/">Return main</a>
                    </p>
                </body>
                </html>
            '''
        )

    item = data_list.pop()
    with open('datajson.json', 'w') as data:
        json.dump(data_list, data)
    return HttpResponse(
        f'''
        <!DOCTYPE html>
        <html>
        <head>
            <!-- CSS only -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
        </head>
        <body>
            <h5>here {item['name']} {item['amount']}</h5>
            <p>
            <a href="/">Return main</a>
            </p>
        </body>
        </html>
        '''
    )




