import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("processed_files", {
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
  file_name: DataTypes.STRING(255),
  encrypt_image:DataTypes.TEXT
  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
