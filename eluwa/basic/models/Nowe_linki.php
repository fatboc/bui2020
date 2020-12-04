<?php

namespace app\models;

use Yii;

/**
 * This is the model class for table "nowe_linki".
 *
 * @property string $data
 * @property string $nazwa
 * @property string $linkk
 */
class Nowe_linki extends \yii\db\ActiveRecord
{
    /**
     * {@inheritdoc}
     */
    public static function tableName()
    {
        return 'nowe_linki';
    }

    /**
     * {@inheritdoc}
     */
    public function rules()
    {
        return [
            [['data', 'nazwa', 'linkk'], 'required'],
            [['data'], 'safe'],
            [['nazwa', 'linkk'], 'string', 'max' => 255],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function attributeLabels()
    {
        return [
            'data' => 'Data',
            'nazwa' => 'Nazwa',
            'linkk' => 'Linkk',
        ];
    }
}
