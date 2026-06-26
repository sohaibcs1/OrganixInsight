import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("immunofluorescent_nc", {
  uuid: {
    // primaryKey: true,
    // type: UUID,
    // defaultValue: UUIDV1
    primaryKey: true,
    type: DataTypes.INTEGER,
    autoIncrement: true
  },

  type: DataTypes.STRING(255),
  type_id: DataTypes.STRING(255),
  location: DataTypes.STRING(255),
  emission: DataTypes.STRING(255),
  cellular_components: DataTypes.STRING(225),
  comment: DataTypes.STRING(225),

  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
