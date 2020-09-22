from  PyAsync import Application, Request, run_app, make_success_response

app = Application()

async def hello_world(request):
    return make_success_response({"message": "Hello World"})

async def test_post(request: Request):
    body =  await request.json()
    return make_success_response({"body": body })

app.router.add_route(
    path="/api", methods_handler={'GET': hello_world, 'POST': test_post}
)

if __name__ == "__main__":
    run_app(app, host='0.0.0.0', port=5001)




