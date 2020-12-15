<?php

namespace app\models;

use yii\db\ActiveRecord;

class Kursy extends ActiveRecord
{
    public static function tableName()
    {
        return 'kursy_prowadzacy';
    }
}
