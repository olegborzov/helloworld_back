# Пример вызова скрипта
# nohup ./ci-cd/rollback.sh dev "123456:ABCDEsaw" "-1001018" "docker.helloworld.com" &

# 1. Устанавливаем из входных параметров переменные окружения
export HW_ENV=$1
export HW_TG_BOT_TOKEN=$2
export HW_TG_CHAT_ID=$3
export HW_DOCKER_REGISTRY=$4  # Хост репозитория Docker
HW_BRANCH=$([ "${HW_ENV?}" "==" "dev" ] && echo master || echo dev)

# 2. Откат деплоя на предыдущую версию
sh ./.ci-cd/curl_tg.sh "#start_rollback"

/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:temp"
/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"
/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:temp" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous"
/usr/local/bin/docker-compose up -d

sh ./.ci-cd/curl_tg.sh "#end_rollback"
