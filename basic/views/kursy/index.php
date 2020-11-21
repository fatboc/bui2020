<?php
use yii\helpers\Html;
use yii\widgets\LinkPager;
?>
<h1>Kursy</h1>
<ul>
<br>
<?php foreach ($kursy as $kurs): ?>
<?= Html::encode("{$kurs->nazwa} ({$kurs->prowadzacy})") ?>
<br>
<br>
<?php endforeach; ?>
</ul>
<?= LinkPager::widget(['pagination' => $pagination]) ?>

