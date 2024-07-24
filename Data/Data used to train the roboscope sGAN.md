# Data used to train the roboscope sGAN:
Data associated with article "The Roboscope: Smart and Fast Microscopy for Generic Event-Driven Acquisition" by J. Bonnet et al. 2024.

Data acquisition: Julia Bonnet, Louis Ruel.  
Data curation: Célia Martin, Claire Déméautis, Julia Bonnet, Louis Ruel, Marc Tramier, Jacques Pécréaux.  
Inscoper, SAS, France.  
CNRS, Univ Rennes, IGDR (Institut de Génétique et Développement de Rennes) – UMR 6290, Rennes, France.  

Datasets creation date: 2024.

License: [CeCILL v2.1, see file Licence_CeCILL_V2.1-en.txt](../LICENSE.txt).

## Balanced Zeiss Dataset
The dataset is split into four subsets (folders) featuring about the same amount of data. This organisation is needed to perform cross-validation of the training as described in the supplementary text. Within these folders, one can find subfolders with cell vignettes. Each subfolder corresponds to a class (mitosis phases mostly), namely:

* **I**nterphase
* **P**rometaphase
*  **P**ro**M**etaphase
*  **M**etaphase
*  **A**naphase
*  **T**elophase
*  **J**unk

We discarded the excess vignettes in some phases so that we have *circa* the same number of vignettes per class (equilibrated). 

## Balanced Zeiss Dataset
The dataset is split into three subsets (folders) featuring about the same amount of data. This is needed to perform cross-validation of the training as described in the supplementary text. Within these folders, one can find subfolders with cell vignettes. Each subfolder corresponds to the same classes as for the Zeiss dataset. We discarded the excess vignettes in some phases so that we have *circa* the same number of vignettes per class (equilibrated). 

