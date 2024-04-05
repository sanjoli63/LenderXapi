import json
orderData ={
    "watchers":[
        123213,
        123213
    ]
}

request= json.dumps({
     "watchers":   ",".join(map(str, orderData['watchers']))
})

print(request)
