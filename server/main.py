from apscheduler.schedulers.background import BackgroundScheduler
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS

from config.setting import AppSetting
from controller.user.user_controller import UserController

app = Sanic()
CORS(app)


@app.route('/api/<module>/<action>', methods=['GET', 'POST', 'OPTIONS'])
async def http_handler(request, module, action):
    process = None
    if module == 'user':
        process = UserController
    return process(request, action).process()


# scheduler = BackgroundScheduler()
# scheduler.add_job(TaskWeixin.run_each_60x5, 'interval', seconds=60 * 5)

if __name__ == "__main__":
    app.run(host=AppSetting.get_host(), port=AppSetting.get_port())
    print("http://" + AppSetting.get_host() + ":" + str(AppSetting.get_port()))