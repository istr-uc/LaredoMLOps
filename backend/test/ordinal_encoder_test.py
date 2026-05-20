import unittest
import pandas as pd
import numpy as np
from src.utils.preprocessing_transfomer import OrdinalEncoderTransformer
from src.utils.preprocessing_data_classes import OrdinalEncoderParams
from src.utils.preprocessing_strategy import OrdinalEncoderStrategy
from sklearn.pipeline import Pipeline


class TestOrdinalEncoderTransformer(unittest.TestCase):
    """Test suite for OrdinalEncoderTransformer with column selection."""
    
    def setUp(self):
        """Create test data."""
        self.data = pd.DataFrame({
            'color': ['red', 'blue', 'red', 'green', np.nan],
            'size': ['small', 'large', 'small', 'medium', 'large'],
            'price': [10.5, 20.0, 15.3, 25.0, 30.0]
        })
    
    def test_encode_specific_columns_only(self):
        """Test that encoder applies to specific columns only."""
        encoder = OrdinalEncoderTransformer(columns=['color', 'size'], unknown_value=-1)
        encoder.fit(self.data)
        result = encoder.transform(self.data)
        result_df = pd.DataFrame(result, columns=self.data.columns)
        
        # Check that color and size are encoded (contain only integers)
        self.assertTrue(all(result_df['color'].apply(lambda x: isinstance(x, (int, np.integer)))))
        self.assertTrue(all(result_df['size'].apply(lambda x: isinstance(x, (int, np.integer)))))
        
        # Check that price is unchanged
        np.testing.assert_array_almost_equal(result_df['price'].values, self.data['price'].values)
    
    def test_nan_maps_to_unknown_value(self):
        """Test that NaN values map to unknown_value."""
        encoder = OrdinalEncoderTransformer(columns=['color'], unknown_value=-1)
        encoder.fit(self.data)
        result = encoder.transform(self.data)
        result_df = pd.DataFrame(result, columns=self.data.columns)
        
        # The last row has NaN in 'color', should be mapped to -1
        self.assertEqual(result_df.iloc[4]['color'], -1)
    
    def test_unseen_categories_map_to_unknown_value(self):
        """Test that unseen categories map to unknown_value."""
        train_data = pd.DataFrame({
            'color': ['red', 'blue', 'red', 'green'],
            'size': ['small', 'large', 'small', 'medium']
        })
        
        test_data = pd.DataFrame({
            'color': ['red', 'yellow'],  # 'yellow' not in training data
            'size': ['small', 'large']
        })
        
        encoder = OrdinalEncoderTransformer(columns=['color'], unknown_value=-1)
        encoder.fit(train_data)
        result = encoder.transform(test_data)
        result_df = pd.DataFrame(result, columns=test_data.columns)
        
        # 'yellow' should map to -1
        self.assertEqual(result_df.iloc[1]['color'], -1)
        # 'red' should map to learned value
        self.assertNotEqual(result_df.iloc[0]['color'], -1)
    
    def test_encode_all_columns_when_none_specified(self):
        """Test backward compatibility: encode all columns when columns=None."""
        data = pd.DataFrame({
            'a': ['x', 'y', 'x'],
            'b': ['p', 'q', 'p']
        })
        
        encoder = OrdinalEncoderTransformer(columns=None, unknown_value=-1)
        encoder.fit(data)
        result = encoder.transform(data)
        result_df = pd.DataFrame(result, columns=data.columns)
        
        # Both columns should be encoded
        self.assertTrue(all(result_df['a'].apply(lambda x: isinstance(x, (int, np.integer)))))
        self.assertTrue(all(result_df['b'].apply(lambda x: isinstance(x, (int, np.integer)))))
    
    def test_custom_unknown_value(self):
        """Test custom unknown_value parameter."""
        encoder = OrdinalEncoderTransformer(columns=['color'], unknown_value=-999)
        encoder.fit(self.data)
        result = encoder.transform(self.data)
        result_df = pd.DataFrame(result, columns=self.data.columns)
        
        # NaN should map to -999
        self.assertEqual(result_df.iloc[4]['color'], -999)


class TestOrdinalEncoderParams(unittest.TestCase):
    """Test suite for OrdinalEncoderParams Pydantic model."""
    
    def test_valid_params(self):
        """Test valid parameter configuration."""
        params = OrdinalEncoderParams(columns=['col1', 'col2'], unknown_value=-1)
        self.assertEqual(params.columns, ['col1', 'col2'])
        self.assertEqual(params.unknown_value, -1)
    
    def test_default_unknown_value(self):
        """Test default unknown_value."""
        params = OrdinalEncoderParams(columns=['col1'])
        self.assertEqual(params.unknown_value, -1)
    
    def test_missing_columns_raises_error(self):
        """Test that missing columns parameter raises validation error."""
        with self.assertRaises(ValueError):
            OrdinalEncoderParams(unknown_value=-1)


class TestOrdinalEncoderStrategy(unittest.TestCase):
    """Test suite for OrdinalEncoderStrategy."""
    
    def test_strategy_creates_correct_encoder(self):
        """Test that strategy creates encoder with correct parameters."""
        strategy = OrdinalEncoderStrategy()
        params = {
            'columns': ['color', 'size'],
            'unknown_value': -1
        }
        step_name, encoder = strategy.get_step(params)
        
        self.assertEqual(step_name, 'OrdinalEncoder')
        self.assertIsInstance(encoder, OrdinalEncoderTransformer)
        self.assertEqual(encoder.columns, ['color', 'size'])
        self.assertEqual(encoder.unknown_value, -1)
    
    def test_strategy_with_custom_unknown_value(self):
        """Test strategy with custom unknown_value."""
        strategy = OrdinalEncoderStrategy()
        params = {
            'columns': ['color'],
            'unknown_value': -999
        }
        _, encoder = strategy.get_step(params)
        
        self.assertEqual(encoder.unknown_value, -999)


class TestOrdinalEncoderInPipeline(unittest.TestCase):
    """Test suite for OrdinalEncoderTransformer in a sklearn pipeline."""
    
    def setUp(self):
        """Create test data."""
        self.X_train = pd.DataFrame({
            'category': ['A', 'B', 'A', 'C'],
            'numeric': [1.0, 2.0, 3.0, 4.0]
        })
        self.y_train = pd.Series([0, 1, 0, 1])
        
        self.X_test = pd.DataFrame({
            'category': ['A', 'D'],
            'numeric': [1.5, 4.5]
        })
    
    def test_pipeline_fit_transform(self):
        """Test that encoder works correctly in a pipeline."""
        from sklearn.preprocessing import StandardScaler
        
        encoder = OrdinalEncoderTransformer(columns=['category'], unknown_value=-1)
        scaler = StandardScaler()
        
        pipeline = Pipeline([
            ('encoder', encoder),
            ('scaler', scaler)
        ])
        
        # Should fit without errors
        result = pipeline.fit_transform(self.X_train)
        self.assertEqual(result.shape, self.X_train.shape)
    
    def test_pipeline_fit_predict(self):
        """Test that encoder works with fit and transform separately."""
        encoder = OrdinalEncoderTransformer(columns=['category'], unknown_value=-1)
        pipeline = Pipeline([
            ('encoder', encoder)
        ])
        
        pipeline.fit(self.X_train)
        result = pipeline.transform(self.X_test)
        
        # Should transform without errors
        self.assertEqual(result.shape, self.X_test.shape)
        # Unseen category 'D' should map to -1
        result_df = pd.DataFrame(result, columns=self.X_test.columns)
        self.assertEqual(result_df.iloc[1]['category'], -1)


if __name__ == '__main__':
    unittest.main()
