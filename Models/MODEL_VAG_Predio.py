def preverVAG(df):    
#%% Importações
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    import pandas as pd
    #%% Separando as features (X) e o target (y)
    
    X = df[['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)', 
            'FimDeSemana', 'HorarioComercial'
            #,'Ligados'
            ]]
    
    y = df['VAG Predio']
    
    #%% Normalização e treinamento
    
    # Dividindo o dataset em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalizando os dados (opcional, mas recomendado para alguns modelos)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Treinando o modelo de regressão linear
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Fazendo previsões
    y_pred = model.predict(X_test)
    
    # Avaliando o modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    #%% Resultados
    print(f'MSE: {mse}')
    print(f'MAE: {mae}')
    print(f'R²: {r2}')
    
    #%% Usando random florest
    
    from sklearn.ensemble import RandomForestRegressor
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Treinando o modelo Random Forest
    model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    model_rf.fit(X_train, y_train)
    
    # Avaliando o modelo
    y_pred_rf = model_rf.predict(X_test)
    mse_rf = mean_squared_error(y_test, y_pred_rf)
    r2_rf = r2_score(y_test, y_pred_rf)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    
    print(f'MSE (Random Forest): {mse_rf}')
    print(f'R² (Random Forest): {r2_rf}')
    print(f'MAE (Random Forest): {mae_rf}')
    # Plotando a importância das variáveis
    importances = model_rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    features = X.columns
    
    plt.figure(figsize=(10,6))
    plt.title("Importância das Features VAG")
    plt.bar(range(X.shape[1]), importances[indices], align="center")
    plt.xticks(range(X.shape[1]), [features[i] for i in indices], rotation=90)
    plt.tight_layout()
    plt.show()

        
    import joblib
    joblib.dump(model_rf, 'ModelsDeploy\VAG.pkl')

#%% Usando Gradient Boosting

    from sklearn.ensemble import GradientBoostingRegressor
    
    model_gbm = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model_gbm.fit(X_train, y_train)
    y_pred_gbm = model_gbm.predict(X_test)
    
    mse_gbm = mean_squared_error(y_test, y_pred_gbm)
    r2_gbm = r2_score(y_test, y_pred_gbm)
    mae_gbm = mean_absolute_error(y_test, y_pred_gbm)
    
    print(f'MSE (GBM): {mse_gbm}')
    print(f'R² (GBM): {r2_gbm}')
    print(f'MAE (GBM): {mae_gbm}')

#%% Usando XGBoost

    import xgboost as xgb
    
    model_xgb = xgb.XGBRegressor(n_estimators=100, random_state=42)
    model_xgb.fit(X_train, y_train)
    y_pred_xgb = model_xgb.predict(X_test)
    
    mse_xgb = mean_squared_error(y_test, y_pred_xgb)
    r2_xgb = r2_score(y_test, y_pred_xgb)
    mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
    
    print(f'MSE (XGBoost): {mse_xgb}')
    print(f'R² (XGBoost): {r2_xgb}')
    print(f'MAE (XGBoost): {mae_xgb}')
    
#%% Usando  LightGBM

    import lightgbm as lgb

    model_lgb = lgb.LGBMRegressor(n_estimators=100, random_state=42)
    model_lgb.fit(X_train, y_train)
    y_pred_lgb = model_lgb.predict(X_test)
    
    mse_lgb = mean_squared_error(y_test, y_pred_lgb)
    r2_lgb = r2_score(y_test, y_pred_lgb)
    mae_lgb = mean_absolute_error(y_test, y_pred_lgb)
    
    print(f'MSE (LightGBM): {mse_lgb}')
    print(f'R² (LightGBM): {r2_lgb}')
    print(f'MAE (LightGBM): {mae_lgb}')

#%% Usando CatBoost

    from catboost import CatBoostRegressor

    model_cat = CatBoostRegressor(n_estimators=100, random_state=42, verbose=0)
    model_cat.fit(X_train, y_train)
    y_pred_cat = model_cat.predict(X_test)
    
    mse_cat = mean_squared_error(y_test, y_pred_cat)
    r2_cat = r2_score(y_test, y_pred_cat)
    mae_cat = mean_absolute_error(y_test, y_pred_cat)
    
    print(f'MSE (CatBoost): {mse_cat}')
    print(f'R² (CatBoost): {r2_cat}')
    print(f'MAE (CatBoost): {mae_cat}')

#%% Usando Support Vector Regression (SVR)

    from sklearn.svm import SVR

    model_svr = SVR(kernel='rbf')
    model_svr.fit(X_train, y_train)
    y_pred_svr = model_svr.predict(X_test)
    
    mse_svr = mean_squared_error(y_test, y_pred_svr)
    r2_svr = r2_score(y_test, y_pred_svr)
    mae_svr = mean_absolute_error(y_test, y_pred_svr)
    
    print(f'MSE (SVR): {mse_svr}')
    print(f'R² (SVR): {r2_svr}')
    print(f'MAE (SVR): {mae_svr}')

#%% Usando Ridge and Lasso Regression

    from sklearn.linear_model import Ridge

    model_ridge = Ridge(alpha=1.0)
    model_ridge.fit(X_train, y_train)
    y_pred_ridge = model_ridge.predict(X_test)
    
    mse_ridge = mean_squared_error(y_test, y_pred_ridge)
    r2_ridge = r2_score(y_test, y_pred_ridge)
    mae_ridge = mean_absolute_error(y_test, y_pred_ridge)
    
    print(f'MSE (Ridge): {mse_ridge}')
    print(f'R² (Ridge): {r2_ridge}')
    print(f'MAE (Ridge): {mae_ridge}')
    
#%% Usando ElasticNet

    from sklearn.linear_model import ElasticNet

    model_en = ElasticNet(alpha=1.0, l1_ratio=0.5)
    model_en.fit(X_train, y_train)
    y_pred_en = model_en.predict(X_test)
    
    mse_en = mean_squared_error(y_test, y_pred_en)
    r2_en = r2_score(y_test, y_pred_en)
    mae_en = mean_absolute_error(y_test, y_pred_en)
    
    print(f'MSE (ElasticNet): {mse_en}')
    print(f'R² (ElasticNet): {r2_en}')
    print(f'MAE (ElasticNet): {mae_en}')


#%% Usando Redes neurais
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.optimizers import Adam
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    
    # Preparar os dados

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalizar os dados
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Definir o modelo
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='linear'))  # Saída para regressão
    
    # Compilar o modelo
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    
    # Treinar o modelo
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, verbose=1)
    
    # Fazer previsões
    y_pred = model.predict(X_test)
    
    # Avaliar o modelo
    mse_nn = mean_squared_error(y_test, y_pred)
    r2_nn = r2_score(y_test, y_pred)
    mae_nn = mean_absolute_error(y_test, y_pred)
    
    print(f'MSE (Neural Network): {mse_nn}')
    print(f'R² (Neural Network): {r2_nn}')
    print(f'MAE (Neural Network): {mae_nn}')

    import matplotlib.pyplot as plt
    
    # Plotar a perda (loss) durante o treinamento e validação
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

#%% Matriz de comparação de modelos    
    data = {
    'Modelo': ['Linear','Random Forest', 'GBM','XGBM','LGBM','CAT','SVR','Ridge','ElasticNet','NN' ],
    'MSE': [mse, mse_rf, mse_gbm, mse_xgb, mse_lgb, mse_cat, mse_svr, mse_ridge, mse_en, mse_nn],
    'R²': [r2, r2_rf, r2_gbm, r2_xgb, r2_lgb, r2_cat, r2_svr, r2_ridge, r2_en, r2_nn],
    'MAE': [mse, mae_rf, mae_gbm, mae_xgb, mae_lgb, mae_cat, mae_svr, mae_ridge, mae_en, mae_nn]}

    df_indicators = pd.DataFrame(data)
    return df_indicators