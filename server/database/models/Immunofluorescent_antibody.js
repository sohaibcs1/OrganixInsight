import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("immunofluorescent_antibody", {
  uuid: {
    // primaryKey: true,
    // type: UUID,
    // defaultValue: UUIDV1
    primaryKey: true,
    type: DataTypes.INTEGER,
    autoIncrement: true
  },

  type: DataTypes.STRING(255),   //Primary or Secondry
  type_id: DataTypes.STRING(255), // name
  emission_frequency: DataTypes.STRING(255), //only if secondry
  comment: DataTypes.STRING(225),
  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
