#You can also change it back to 1.00
DAL_GAMMA_SCALE=0.95
SRC_INPUT_FILE=REPRODUCIBLE/norm.iwslt17.dev2010.de

for SETUP in REAL INSEG OUTSEG_INSEG POLICY_OUTSEG_INSEG;
do
    echo $SETUP
    for k in 1 2 3 4 5 6 7 8 9 10;

    do
        ACTION_FILE=REPRODUCIBLE/$SETUP/$k.RW
        RESEGMENTED_H=REPRODUCIBLE/$SETUP/$k.reseg_h
        echo $k $(python3 eval_streaming_latency.py $SRC_INPUT_FILE $RESEGMENTED_H $ACTION_FILE $DAL_GAMMA_SCALE)
    done

done
