echo PyFlightCoach conda environment creations
echo use existing environment? y/n

read varname

if [ $varname == "n" ]; then
    echo enter new env name
    read envname

    conda create -n $envname python=3.12 --yes 
    conda init bash
    conda activate $envname
fi

source install_submodules.sh

while read requirement; 
do 
    conda install --yes -c conda-forge $requirement || pip install $requirement 
done < requirements_plot.txt

