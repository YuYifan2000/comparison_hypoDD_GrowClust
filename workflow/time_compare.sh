START=`date +%s`
ph2dt ph2dt.inp
hypoDD hypodd_ct.inp
END=`date +%s`
DIFF1=$(( $END - $START ))

START=`date +%s`
growclust gc.inp
END=`date +%s`
DIFF2=$(( $END - $START ))


START=`date +%s`
hyp1.40 < hyp.command
END=`date +%s`
DIFF3=$(( $END - $START ))



echo "hypodd took $DIFF1 seconds"
echo "GC took $DIFF2 seconds"
echo "hypoinver took $DIFF3 seconds"
