DAL_GAMMA_SCALE=1.00
SRC_INPUT_FILE=REPRODUCIBLE/norm.iwslt17.dev2010.de

awk '$1=$1' ORS=' ' $SRC_INPUT_FILE > 1-line.src

for SETUP in REAL INSEG OUTSEG_INSEG POLICY_OUTSEG_INSEG;
do
    echo $SETUP
    for k in 1 2 3 4 5 6 7 8 9 10;
    do
        ACTION_FILE=REPRODUCIBLE/$SETUP/$k.RW
        RESEGMENTED_H=REPRODUCIBLE/$SETUP/$k.reseg_h
        awk '$1=$1' ORS=' ' $RESEGMENTED_H > 1-line.reseg
        echo $k $(python3 eval_streaming_latency_old.py $PWD/1-line.src $PWD/1-line.reseg $ACTION_FILE $DAL_GAMMA_SCALE)
    done

done
