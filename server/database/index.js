import Sequelize from 'sequelize';
import { connectionString } from './config.js';
import UserModel from './models/User.js';
import BiospecimenModel from './models/Biospecimen_e_f_c.js';
import Biospecimen_org_pdx from './models/Biospecimen_org_pdx.js';
import Biospecimen_tumor from './models/Biospecimen_tumor.js';

import Perturbagens_DSR from './models/Perturbagens_DSR.js';

import Immunofluorescent_nc from './models/Immunofluorescent_nc.js';
import Immunofluorescent_antibody from './models/Immunofluorescent_antibody.js';
import Study from './models/Study.js';
import Experiment from './models/Experiment.js';
import File from './models/File.js';
import File_bulk from './models/File_bulk.js';

import Processed_files from './models/Processed_files.js';
import Model_files from './models/Model_files.js';
import Model_2d from './models/Model_2d.js';
import Model_2d_prot from './models/Model_2d_prot.js';

export const sequelize = new Sequelize(connectionString);


const User = UserModel(sequelize);
const Biospecimen= BiospecimenModel(sequelize);
const biospecimen_org_pdx=Biospecimen_org_pdx(sequelize);
const biospecimen_tumor=Biospecimen_tumor(sequelize);
const perturbagens_DSR=Perturbagens_DSR(sequelize);

const immunofluorescent_nc=Immunofluorescent_nc(sequelize);
const immunofluorescent_antibody=Immunofluorescent_antibody(sequelize);

const study=Study(sequelize);
const experiment=Experiment(sequelize);
const file=File(sequelize);
const file_bulk=File_bulk(sequelize);
const processed_files=Processed_files(sequelize);
const model_files=Model_files(sequelize);
const model_2d=Model_2d(sequelize);
const model_2d_prot=Model_2d_prot(sequelize);


const init = async () => {
  try {
    await sequelize.authenticate();
    console.info('Connection to database has been established successfully.');

    //Relations
      //Define Association/Relations between tables


//comment start

    // sequelize.sync(
    //   { force: true }
    // );


    //comment End

  } catch (error) {
    console.error('Unable to connect to the database:', error);
  }
}

export {
  init, User, Biospecimen,biospecimen_org_pdx,biospecimen_tumor,perturbagens_DSR,immunofluorescent_nc,immunofluorescent_antibody,
  study,experiment,file,file_bulk,processed_files,model_files,model_2d,model_2d_prot
}
