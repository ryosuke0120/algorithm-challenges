#!/bin/bash

timeout() {
    time=$1
    # start the command in a subshell to avoid problem with pipes
    # (spawn accepts one command)
    command="/bin/sh -c \"${@:2}\""
    expect -c "set timeout $time; spawn -noecho $command; expect timeout { exit 124 } eof; catch wait result; exit [lindex \$result 3]"
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <testcase_number>"
    exit 1
fi

TESTCASE_NUMBER=$1
TESTCASE_PATH="./testcase/case${TESTCASE_NUMBER}.txt"
EXPECTED_ANSWER_PATH="./testcase/answer${TESTCASE_NUMBER}.txt"

echo "Testcase $TESTCASE_NUMBER"

# テストケースを読み込む
TESTCASE_CONTENT=$(cat "$TESTCASE_PATH")

# 実行時間を16秒に設定して main.py を実行
timeout 16 python main.py < "$TESTCASE_PATH"

# 結果と実行時間を抽出する
RESULT_VALUE=$(python main.py < "$TESTCASE_PATH")

# 期待される答えを読み取る
EXPECTED_ANSWER=$(cat "$EXPECTED_ANSWER_PATH")

# 結果と期待される答えを比較して判定
if [ "$RESULT_VALUE" = "$EXPECTED_ANSWER" ]; then
    JUDGEMENT="Successed"
else
    JUDGEMENT="Failed"
fi

# 結果を出力
echo "-----------------"
echo "Expected: $EXPECTED_ANSWER"
echo "Your answer: $RESULT_VALUE"
echo "-----------------"
echo "Judge : $JUDGEMENT"
