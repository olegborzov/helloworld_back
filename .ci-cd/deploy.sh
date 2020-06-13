# Пример вызова скрипта
# nohup ./ci-cd/deploy.sh dev docker.helloworld.com "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw" "-1001234567890"

# 1. Устанавливаем из входных параметров переменные окружения
export HW_ENV=$1
HW_BRANCH=$([ "${HW_ENV?}" "==" "dev" ] && echo master || echo dev)
export HW_DOCKER_REGISTRY=$4  # Хост репозитория Docker
HW_TG_BOT_TOKEN=$2
HW_TG_CHAT_ID=$3

# 2. Деплой
sh ./.ci-cd/curl_tg.sh "$HW_TG_BOT_TOKEN" "$HW_TG_CHAT_ID" "$HW_ENV" "#deploy_start"

/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous"
/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:new" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"
/usr/local/bin/docker-compose -p "hw_back_${HW_ENV}" up -d  --remove-orphans

sh ./.ci-cd/curl_tg.sh "$HW_TG_BOT_TOKEN" "$HW_TG_CHAT_ID" "$HW_ENV" "#deploy_success"

