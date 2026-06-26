import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("model_2d", {
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
  random_id: DataTypes.STRING(255),
  file_name: DataTypes.STRING(255),
  cell_count: DataTypes.STRING(255),

  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
