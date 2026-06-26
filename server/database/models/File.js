import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("file", {
  uuid: {
    // primaryKey: true,
    // type: UUID,

    // defaultValue: UUIDV1
    primaryKey: true,
    type: DataTypes.INTEGER,
    autoIncrement: true
  },

  study_id: DataTypes.STRING(255),
  experiment_id: DataTypes.STRING(255),
  ex_type: DataTypes.STRING(255),
  phase_info: DataTypes.STRING(255),
  cell_count: DataTypes.STRING(255),
  counterstain: DataTypes.STRING(255),
  file_addr: DataTypes.STRING(255),
  file_type: DataTypes.STRING(255),
  file_size:DataTypes.STRING(255),
  file_meta:DataTypes.TEXT,
  deconvolve:DataTypes.STRING(255),
  process:DataTypes.STRING(255),
  random_id:DataTypes.STRING(255),
  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
