# Пример вызова скрипта
# nohup sh .ci-cd/rollback.sh dev docker.helloworld.com "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw" "-1001234567890"

# 1. Устанавливаем из входных параметров переменные окружения
export HW_ENV=$1
HW_BRANCH=$([ "${HW_ENV?}" "==" "prod" ] && echo master || echo dev)
export HW_DOCKER_REGISTRY=$2  # Хост репозитория Docker
HW_TG_BOT_TOKEN=$3
HW_TG_CHAT_ID=$4

# 2. Откат деплоя на предыдущую версию
sh ./.ci-cd/curl_tg.sh "$HW_TG_BOT_TOKEN" "$HW_TG_CHAT_ID" "$HW_ENV" "#start_rollback"

/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:temp"
/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"
/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:temp" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous"
/usr/local/bin/docker-compose up -d

sh ./.ci-cd/curl_tg.sh "$HW_TG_BOT_TOKEN" "$HW_TG_CHAT_ID" "$HW_ENV" "#end_rollback"
