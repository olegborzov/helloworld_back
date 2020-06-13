# Пример вызова скрипта
# nohup bash .ci-cd/deploy.sh \
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


# 2. Авторизация в репозитории Docker
/usr/bin/docker login "${HW_DOCKER_REGISTRY}" -u "$HW_DOCKER_LOGIN" -p "${HW_DOCKER_PASSWORD}"


# 3. Запуск миграций
sh ./.ci-cd/curl_tg.sh "$HW_TG_BOT_TOKEN" "$HW_TG_CHAT_ID" "$HW_ENV" "#migration_start"
/usr/bin/docker run --rm \
  --env-file "conf/.env_files/${HW_ENV}.env" \
  "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:new" \
  sh -c "flask db upgrade"
migration_result=$?

if [ $migration_result != 0 ]; then
  sh ./.ci-cd/curl_tg.sh "#migration_failed"
  exit 1
fi


# 4. Деплой
sh ./.ci-cd/curl_tg.sh "$HW_TG_BOT_TOKEN" "$HW_TG_CHAT_ID" "$HW_ENV" "#deploy_start"

/usr/bin/docker pull "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:new"
/usr/bin/docker pull "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"

/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous"
/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:new" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"

/usr/bin/docker push "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous"
/usr/bin/docker push "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"

/usr/local/bin/docker-compose -p "hw_back_${HW_ENV}" up -d  --remove-orphans

sh ./.ci-cd/curl_tg.sh "$HW_TG_BOT_TOKEN" "$HW_TG_CHAT_ID" "$HW_ENV" "#deploy_success"

