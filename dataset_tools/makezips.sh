
MYPWD=$(pwd)
FOLDER="/home/asvin/git/long-video-gan-az/datasets/flower"

cd $FOLDER
for RES in $(ls -d */)
do 
    echo $RES
    CURRPATH="$FOLDER/$RES"
    FILEPATH="partition_0000.zip"
    DESTPATH="$FOLDER/../flowerzip/$RES/partition_0000.zip"
    cd $CURRPATH
    # Need to make zip files from directory that has folders for all clips
    rm $FILEPATH
    zip -r -q -0 $FILEPATH .
    zip -d -q $FILEPATH \*/
    cp $FILEPATH $DESTPATH
    cd ..
done

cd $MYPWD