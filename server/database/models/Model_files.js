import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("model_files", {
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
  image_combined_file: DataTypes.STRING(255),
  model_prediction_files:DataTypes.STRING(255),
  model_prediction_mask:DataTypes.STRING(255),
  mask_file_analysis:DataTypes.TEXT,
  basal:DataTypes.TEXT,
  positive:DataTypes.TEXT

  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
