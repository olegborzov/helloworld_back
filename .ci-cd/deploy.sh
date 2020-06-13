# Пример вызова скрипта
# nohup ./ci-cd/deploy.sh dev "123456:ABCDEsaw" "-1001018" &

# 1. Устанавливаем из входных параметров переменные окружения
export HW_ENV=$1            # Окружение (dev/prod)
export HW_TG_BOT_TOKEN=$2   # Токен бота Telegram (пример - bot110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw)
export HW_TG_CHAT_ID=$3     # ID чата/канала в Telegram, куда бот будет отправлять сообщения (пример -1001234567890)

# 2. Деплой
sh ./.ci-cd/curl_tg.sh "#deploy_start"

docker tag "hw_back_${HW_ENV}:latest" "hw_back_${HW_ENV}:previous"
docker tag "hw_back_${HW_ENV}:new" "hw_back_${HW_ENV}:latest"
docker-compose -p "hw_back_${HW_ENV}" up -d  --remove-orphans

sh ./.ci-cd/curl_tg.sh "#deploy_success"

