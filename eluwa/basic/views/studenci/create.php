<?php

use yii\helpers\Html;

/* @var $this yii\web\View */
/* @var $model app\models\Studenci */

$this->title = 'Create Studenci';
$this->params['breadcrumbs'][] = ['label' => 'Studencis', 'url' => ['index']];
$this->params['breadcrumbs'][] = $this->title;
?>
<div class="studenci-create">

    <h1><?= Html::encode($this->title) ?></h1>

    <?= $this->render('_form', [
        'model' => $model,
    ]) ?>

</div>
