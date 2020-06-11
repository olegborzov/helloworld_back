# Пример вызова скрипта
# nohup ./ci-cd/deploy.sh dev "123456:ABCDEsaw" "-1001018" &

# 1. Устанавливаем из входных параметров переменные окружения
export HW_ENV=$1
export HW_TG_BOT_TOKEN=$2
export HW_TG_CHAT_ID=$3
printf "\n\n### %s - start_deploy###\n" "$(date)" >> dockerlog.txt


# 2. Запускаем билд
sh ./.ci-cd/curl_tg.sh "#start_build"
docker build -f ./conf/docker/Dockerfile -t "hw_back_${HW_ENV}:new" . 2>> dockerlog.txt
build_result=$?
printf "\nBUILD result %s\n" "$build_result"

if [ "$build_result" != 0 ]; then
  sh ./.ci-cd/curl_tg.sh "#build_failed"
  docker image rm "hw_back_${HW_ENV}:new"
  exit 1
fi


# 3. Запускаем тесты
sh ./.ci-cd/curl_tg.sh "#start_tests"
sh ./.ci-cd/run_tests.sh
tests_result=$?
printf "\nTEST result %s\n" "$tests_result"

if [ "$tests_result" != 0 ]; then
  sh ./.ci-cd/curl_tg.sh "#tests_failed"
  docker image rm "hw_back_${HW_ENV}:new"
  exit 1
fi


# 4. Запуск миграций
docker run --rm --env-file "conf/.env_files/${HW_ENV}.env" "hw_back_${HW_ENV}:new" sh -c "flask db upgrade" 2>> dockerlog.txt
migration_result=$?
printf "\nMIGRATION result %s\n" "$migration_result"

if [ $migration_result != 0 ]; then
  sh ./.ci-cd/curl_tg.sh "#migration_failed"
  docker image rm "hw_back_${HW_ENV}:new"
  exit 1
fi


# 5. Деплой
docker tag "hw_back_${HW_ENV}:latest" "hw_back_${HW_ENV}:previous"
docker tag "hw_back_${HW_ENV}:new" "hw_back_${HW_ENV}:latest"
docker-compose -p "hw_back_${HW_ENV}" up -d  --remove-orphans

sh ./.ci-cd/curl_tg.sh "#deploy_success"

