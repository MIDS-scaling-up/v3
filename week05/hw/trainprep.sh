#!/bin/sh

for f in `ls *.tar`
do

  bf=`basename $f .tar`
  echo $bf
  mkdir $bf
  mv $f $bf
  cd $bf
  tar -xf $f
  rm $f
  cd ..
done
