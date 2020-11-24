<?php

namespace app\models;

use Yii;

/**
 * This is the model class for table "studenci".
 *
 * @property int $nr_indeksu
 * @property string $imie
 * @property string $nazwisko
 *
 * @property KursyStudenci[] $kursyStudencis
 * @property Kursy[] $nrKursus
 */
class Studenci extends \yii\db\ActiveRecord
{
    /**
     * {@inheritdoc}
     */
    public static function tableName()
    {
        return 'studenci';
    }

    /**
     * {@inheritdoc}
     */
    public function rules()
    {
        return [
            [['nr_indeksu', 'imie', 'nazwisko'], 'required'],
            [['nr_indeksu'], 'integer'],
            [['imie', 'nazwisko'], 'string', 'max' => 16],
            [['nr_indeksu'], 'unique'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function attributeLabels()
    {
        return [
            'nr_indeksu' => 'Nr Indeksu',
            'imie' => 'Imie',
            'nazwisko' => 'Nazwisko',
        ];
    }

    /**
     * Gets query for [[KursyStudencis]].
     *
     * @return \yii\db\ActiveQuery
     */
    public function getKursyStudencis()
    {
        return $this->hasMany(KursyStudenci::className(), ['nr_indeksu' => 'nr_indeksu']);
    }

    /**
     * Gets query for [[NrKursus]].
     *
     * @return \yii\db\ActiveQuery
     */
    public function getNrKursus()
    {
        return $this->hasMany(Kursy::className(), ['nr_kursu' => 'nr_kursu'])->viaTable('kursy_studenci', ['nr_indeksu' => 'nr_indeksu']);
    }
}
