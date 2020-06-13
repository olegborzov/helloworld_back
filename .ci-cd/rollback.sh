# Пример вызова скрипта
# nohup bash .ci-cd/rollback.sh \
#   dev \
#   docker.helloworld.com \
#   docker_user \
#   docker_password \
#   "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw" \
#   "-1001234567890"


# 1. Устанавливаем из входных параметров переменные окружения
export HW_ENV=$1
HW_BRANCH=$([ "${HW_ENV?}" == 'prod' ] && echo master || echo dev)
export HW_BRANCH
export HW_DOCKER_REGISTRY=$2  # Хост репозитория Docker
HW_DOCKER_LOGIN=$3            # Логин для репозитория Docker
HW_DOCKER_PASSWORD=$4         # Пароль для репозитория Docker
HW_TG_BOT_TOKEN=$5            # Токен для бота Telegram
HW_TG_CHAT_ID=$6              # ID чата/канала в Telegram для отправки уведомлений


# 2. Откат деплоя на предыдущую версию
sh ./.ci-cd/curl_tg.sh "$HW_TG_BOT_TOKEN" "$HW_TG_CHAT_ID" "$HW_ENV" "#start_rollback"

/usr/bin/docker login "${HW_DOCKER_REGISTRY}" -u "$HW_DOCKER_LOGIN" -p "${HW_DOCKER_PASSWORD}"

/usr/bin/docker pull "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"
/usr/bin/docker pull "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous"

/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:temp"
/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"
/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:temp" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous"

/usr/bin/docker push "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"
/usr/bin/docker push "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous"

/usr/local/bin/docker-compose up -d

sh ./.ci-cd/curl_tg.sh "$HW_TG_BOT_TOKEN" "$HW_TG_CHAT_ID" "$HW_ENV" "#end_rollback"
